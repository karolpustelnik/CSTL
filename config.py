conf = {
    "WORK_PATH": "/home/biox/Desktop/biox/CSTL/work",
    "CUDA_VISIBLE_DEVICES": "1, 0",
    "data": {
        'dataset_path': "/home/biox/Desktop/biox/gait_models/datasets/CASIA-Biox/sil2", #your_dataset_path
        'resolution': '64',
        'dataset': 'CASIA-B',
        # In CASIA-B, data of subject #5 is incomplete.
        # Thus, we ignore it in training.
        'pid_num': 73,
        'pid_shuffle': False,
    },
    "model": {
        'hidden_dim': 128,
        'lr': 1e-4,
        'hard_or_full_trip': 'full',
        'batch_size': (8, 8),
        'restore_iter': 0,
        'total_iter': 100_000,
        'margin': 0.2,
        'num_workers': 1,
        'frame_num': 30,
        'model_name': 'CSTL',
    },
}
