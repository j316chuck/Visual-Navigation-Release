import tensorflow as tf
import numpy as np
from planners.planner import Planner
from trajectory.trajectory import Trajectory, SystemConfig


class SamplingPlanner(Planner):
    """ A planner which selects an optimal waypoint using
    a sampling based method. Given a fixed start_config,
    the planner
        1. Uses a control pipeline to plan paths from start_config
            to a fixed set of waypoint configurations
        2. Evaluates the objective function on the resulting trajectories
        3. Returns the minimum cost waypoint and associated trajectory"""

    def optimize(self, start_config):
        """ Optimize the objective over a trajectory
        starting from start_config.
            1. Uses a control pipeline to plan paths from start_config
            2. Evaluates the objective function on the resulting trajectories
            3. Return the minimum cost waypoint, trajectory, and cost
        """
        obj_vals, data = self.eval_objective(start_config)
        min_idx = tf.argmin(obj_vals)
        min_cost = obj_vals[min_idx]

        waypts, horizons_s, trajectories, controllers = data

        self.opt_waypt.assign_from_config_batch_idx(waypts, min_idx)
        self.opt_traj.assign_from_trajectory_batch_idx(trajectories, min_idx)

        # Convert horizon in seconds to horizon in # of steps
        min_horizon = int(tf.ceil(horizons_s[min_idx, 0]/self.params.dt).numpy())
        min_controllers = {'K_1kfd': controllers['K_nkfd'][min_idx:min_idx+1],
                           'k_1kf1': controllers['k_nkf1'][min_idx:min_idx+1]}

        return self.opt_waypt, self.opt_traj, min_cost, min_horizon, min_controllers
