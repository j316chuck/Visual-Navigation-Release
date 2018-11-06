from dotmap import DotMap
from utils import utils
import numpy as np
from costs.quad_cost_with_wrapping import QuadraticRegulatorRef
from trajectory.spline.spline_3rd_order import Spline3rdOrder
from systems.dubins_v2 import DubinsV2
from control_pipelines.control_pipeline_v0 import ControlPipelineV0

dependencies = ['waypoint_params']


def load_params():
    # Load the dependencies
    p = DotMap({dependency: utils.load_params(dependency)
                for dependency in dependencies})

    p.pipeline = ControlPipelineV0

    # The directory for saving the control pipeline files
    p.dir = './data/control_pipelines'

    # Spline parameters
    p.spline_params = DotMap(spline=Spline3rdOrder,
                             max_final_time=6.0,
                             epsilon=1e-5)

    # System Dynamics params
    p.system_dynamics_params = DotMap(system=DubinsV2,
                                      dt=.05,
                                      v_bounds=[0.0, .6],
                                      w_bounds=[-1.1, 1.1])

    # LQR setting parameters
    p.lqr_params = DotMap(cost_fn=QuadraticRegulatorRef,
                          quad_coeffs=np.array(
                              [1.0, 1.0, 1.0, 1e-10, 1e-10], dtype=np.float32),
                          linear_coeffs=np.zeros((5), dtype=np.float32))

    # Velocity binning parameters
    p.binning_parameters = DotMap(num_bins=3,
                                  max_speed=p.system_dynamics_params.v_bounds[1])

    p.verbose = True
    return p


def parse_params(p):
    p.planning_horizon_s = p.spline_params.max_final_time
    p.planning_horizon = int(
        np.ceil(p.planning_horizon_s / p.system_dynamics_params.dt))
    return p
