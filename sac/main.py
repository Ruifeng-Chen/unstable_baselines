import os
import gym
import matplotlib as plt
import click
from common.logger import Logger
from sac.trainer import SACTrainer
from sac.models import SACAgent
from common.util import set_device, update_parameters, load_config
from common.buffer import ReplayBuffer
from sac.wrapper import SACWrapper


@click.command()
@click.argument("config-path",type=str)
@click.option("--log-dir", default="logs")
@click.option("--gpu-id", type=int, default=-1)
@click.option("--print-log", type=bool, default=True)
def main(config_path, log_dir, gpu_id, print_log, **kwargs):
    #todo: add load and update parameters function
    args = load_config(config_path, kwargs)
    #initialize device
    set_device(gpu_id)

    #initialize logger
    env_name = args['env_name']
    logger = Logger(log_dir, prefix = env_name, print_to_terminal=print_log)
    logger.log_str("logging to {}".format(logger.log_path))

    #initialize environment
    env = gym.make(env_name)
    env = SACWrapper(env, **args['env'])
    state_space = env.observation_space
    action_space = env.action_space

    #initialize buffer
    buffer = ReplayBuffer(state_space, action_space, **args['buffer'])

    #initialize agent
    logger.log_str("Initializing Agent")
    agent = SACAgent(state_space, action_space, **args['agent'])

    #initialize trainer
    logger.log_str("Initializing Trainer")
    trainer  = SACTrainer(
        agent,
        env,
        buffer,
        logger,
        **args['trainer']
    )
    
    logger.log_str("Started training")
    trainer.train()


if __name__ == "__main__":
    main()