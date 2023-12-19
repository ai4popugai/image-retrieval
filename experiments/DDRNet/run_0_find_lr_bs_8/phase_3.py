import os

from experiments.DDRNet.run_base import RunBase
from optim_utils.iter_policy.linear_policy import LinearIterationPolicy


class Phase(RunBase):
    def __init__(self):
        super().__init__(os.path.abspath(__file__))

        self.batch_size = 8
        self.num_workers = 4

        self.train_iters = 1000
        self.batch_dump_iters = 1000
        self.snapshot_iters = 1000
        self.show_iters = 10

        self.optimizer_kwargs = {'lr': 0., 'weight_decay': 3e-5}
        self.lr_policy = LinearIterationPolicy(start_iter=40000, start_val=6e-3, end_iter=60000, end_val=9e-3)


if __name__ == '__main__':
    Phase().train(start_snapshot=None)