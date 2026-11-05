"""Check the installed Tide Sidecar and runtime without opening hardware."""

import argparse
import hashlib
import importlib
import importlib.metadata
import json
import os
from pathlib import Path
import platform
import subprocess
import sys
import tempfile


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--sidecar-root', required=True, type=Path)
    parser.add_argument('--download-act', action='store_true',
                        help='Explicitly download missing ACT backbone weights')
    parser.add_argument('--smolvla', action='store_true',
                        help='Also verify the pinned SmolVLA local snapshots')
    parser.add_argument('--download-smolvla', action='store_true',
                        help='Explicitly download the two pinned SmolVLA snapshots')
    args = parser.parse_args()
    root = args.sidecar_root.expanduser().resolve()
    if not (root / 'collector_agent' / 'training.py').is_file():
        parser.error('sidecar-root must contain the bundled collector_agent/training.py')
    sys.path.insert(0, str(root))
    from collector_agent.training import _training_environment, _huggingface_home
    training_env = _training_environment()
    print(json.dumps({
        'python': sys.executable, 'prefix': sys.prefix,
        'resolved_prefix': str(Path(sys.prefix).resolve()),
        'architecture': platform.machine(), 'sidecar_root': str(root),
        'TORCH_HOME': training_env['TORCH_HOME'], 'HF_HOME': str(_huggingface_home()),
    }, indent=2, ensure_ascii=False))
    os.environ.update(training_env)
    if args.download_smolvla:
        os.environ['HF_HUB_OFFLINE'] = '0'
    failures = []

    def check(label, operation):
        try:
            detail = operation()
            print(f'PASS {label}' + (f': {detail}' if detail is not None else ''))
        except Exception as exc:
            failures.append(label)
            print(f'FAIL {label}: {type(exc).__name__}: {exc}')

    def versions():
        assert sys.version_info[:2] == (3, 12), 'Python 3.12 required'
        assert importlib.metadata.version('lerobot') == '0.6.0'
        return {name: importlib.metadata.version(name) for name in (
            'lerobot', 'torch', 'torchvision', 'av', 'opencv-python',
            'cv2-enumerate-cameras', 'pyserial', 'accelerate')}

    check('versions', versions)
    for name in (
        'cv2', 'cv2_enumerate_cameras', 'serial', 'h5py', 'websockets',
        'av', 'pyarrow', 'datasets', 'accelerate',
        'lerobot.scripts.lerobot_record', 'lerobot.scripts.lerobot_train',
        'lerobot.scripts.lerobot_rollout',
        'collector_agent.so101.persistent_runtime',
        'collector_agent.model_rollout_runtime',
    ):
        check(f'import {name}', lambda name=name: (importlib.import_module(name), None)[1])

    def accelerator():
        import torch
        from lerobot.utils.device_utils import auto_select_torch_device
        device = auto_select_torch_device()
        result = (torch.ones(4, device=device) * 2).sum().item()
        assert result == 8
        return str(device)

    check('LeRobot accelerator tensor operation', accelerator)

    def video_roundtrip():
        import av
        import numpy as np
        from lerobot.configs.video import rgb_encoder_defaults
        codec = rgb_encoder_defaults().vcodec
        with tempfile.TemporaryDirectory(prefix='tide-video-check-') as directory:
            filename = str(Path(directory) / 'probe.mp4')
            with av.open(filename, 'w') as container:
                stream = container.add_stream(codec, rate=30)
                stream.width = stream.height = 64
                stream.pix_fmt = 'yuv420p'
                if codec == 'libsvtav1':
                    stream.options = {'preset': '12', 'svtav1-params': 'lp=1'}
                for index in range(3):
                    frame = av.VideoFrame.from_ndarray(
                        np.full((64, 64, 3), index * 50, dtype=np.uint8), format='rgb24')
                    for packet in stream.encode(frame):
                        container.mux(packet)
                for packet in stream.encode():
                    container.mux(packet)
            with av.open(filename) as container:
                assert len(list(container.decode(video=0))) == 3, 'Decoded frame count mismatch'
        return codec

    check('LeRobot default video codec encode/decode', video_roundtrip)

    def act_weights():
        import torch
        from torchvision.models import ResNet18_Weights, resnet18
        from lerobot.policies.act.configuration_act import ACTConfig
        config = ACTConfig()
        assert config.vision_backbone == 'resnet18'
        assert config.pretrained_backbone_weights == 'ResNet18_Weights.IMAGENET1K_V1'
        weights = ResNet18_Weights.IMAGENET1K_V1
        filename = weights.url.rsplit('/', 1)[-1]
        checkpoint = Path(torch.hub.get_dir()) / 'checkpoints' / filename
        if not checkpoint.is_file() and args.download_act:
            weights.get_state_dict(progress=True, check_hash=True)
        if not checkpoint.is_file():
            raise FileNotFoundError(f'{checkpoint}; use --download-act after authorizing download')
        with checkpoint.open('rb') as handle:
            digest = hashlib.file_digest(handle, 'sha256').hexdigest()
        expected = filename.rsplit('-', 1)[-1].split('.')[0]
        assert digest.startswith(expected), 'Backbone checksum mismatch'
        state = torch.load(checkpoint, map_location='cpu', weights_only=True)
        resnet18(weights=None).load_state_dict(state)
        return str(checkpoint)

    check('ACT backbone cache checksum and load', act_weights)
    if args.smolvla or args.download_smolvla:
        def smolvla_weights():
            from collector_agent.training import (
                _smolvla_base_snapshot, SMOLVLA_BASE_REPO, SMOLVLA_BASE_REVISION,
                SMOLVLA_VLM_REPO, SMOLVLA_VLM_REVISION,
            )
            if args.download_smolvla:
                from huggingface_hub import snapshot_download
                for repo, revision in (
                    (SMOLVLA_BASE_REPO, SMOLVLA_BASE_REVISION),
                    (SMOLVLA_VLM_REPO, SMOLVLA_VLM_REVISION),
                ):
                    snapshot_download(repo_id=repo, revision=revision,
                                      cache_dir=str(_huggingface_home() / 'hub'))
            return str(_smolvla_base_snapshot())
        check('SmolVLA pinned local snapshots', smolvla_weights)
    pip_check = subprocess.run([sys.executable, '-m', 'pip', 'check'], capture_output=True, text=True)
    if pip_check.returncode:
        failures.append('pip check')
    print(('PASS' if not pip_check.returncode else 'FAIL') + ' pip check')
    print((pip_check.stdout + pip_check.stderr).strip())
    print('Pending: app-selected interpreter, real capture, training backward/checkpoint, model inference and teardown.')
    print(json.dumps({'failed_checks': failures, 'environment_checks_passed': not failures}))
    return 1 if failures else 0


if __name__ == '__main__':
    raise SystemExit(main())
