from pettingzoo.atari import basketball_pong_v0
from pettingzoo.atari import boxing_v0
from pettingzoo.atari import combat_plane_v0
from pettingzoo.atari import combat_tank_v0
from pettingzoo.atari import double_dunk_v1
from pettingzoo.atari import entombed_competitive_v1
from pettingzoo.atari import entombed_cooperative_v0
from pettingzoo.atari import flag_capture_v0
from pettingzoo.atari import foozpong_v0
from pettingzoo.atari import ice_hockey_v0
from pettingzoo.atari import joust_v1
from pettingzoo.atari import mario_bros_v1
from pettingzoo.atari import maze_craze_v1
from pettingzoo.atari import othello_v1
from pettingzoo.atari import pong_v0
from pettingzoo.atari import quadrapong_v1
from pettingzoo.atari import space_invaders_v0
from pettingzoo.atari import space_war_v0
from pettingzoo.atari import surround_v0
from pettingzoo.atari import tennis_v1
from pettingzoo.atari import video_checkers_v1
from pettingzoo.atari import volleyball_pong_v0
from pettingzoo.atari import wizard_of_wor_v1
from pettingzoo.atari import warlords_v1

from pettingzoo.classic import chess_v0
from pettingzoo.classic import checkers_v0
from pettingzoo.classic import rps_v0
from pettingzoo.classic import rpsls_v0
from pettingzoo.classic import connect_four_v0
from pettingzoo.classic import tictactoe_v0
from pettingzoo.classic import leduc_holdem_v0
from pettingzoo.classic import mahjong_v0
from pettingzoo.classic import texas_holdem_v0
from pettingzoo.classic import texas_holdem_no_limit_v0
from pettingzoo.classic import uno_v0
from pettingzoo.classic import dou_dizhu_v0
from pettingzoo.classic import gin_rummy_v0
from pettingzoo.classic import go_v0
from pettingzoo.classic import hanabi_v0
from pettingzoo.classic import backgammon_v0

from pettingzoo.butterfly import knights_archers_zombies_v2
from pettingzoo.butterfly import pistonball_v0
from pettingzoo.butterfly import cooperative_pong_v1
from pettingzoo.butterfly import prison_v1
from pettingzoo.butterfly import prospector_v2

from pettingzoo.magent import battle_v1
from pettingzoo.magent import adversarial_pursuit_v1
from pettingzoo.magent import gather_v1
from pettingzoo.magent import combined_arms_v1
from pettingzoo.magent import tiger_deer_v1
from pettingzoo.magent import battlefield_v1

from pettingzoo.mpe import simple_adversary_v1
from pettingzoo.mpe import simple_crypto_v1
from pettingzoo.mpe import simple_push_v1
from pettingzoo.mpe import simple_reference_v1
from pettingzoo.mpe import simple_speaker_listener_v2
from pettingzoo.mpe import simple_spread_v1
from pettingzoo.mpe import simple_tag_v1
from pettingzoo.mpe import simple_world_comm_v1
from pettingzoo.mpe import simple_v1

from pettingzoo.sisl import pursuit_v1
from pettingzoo.sisl import waterworld_v1
from pettingzoo.sisl import multiwalker_v3

all_prefixes = ["atari", "classic", "butterfly", "magent", "mpe", "sisl"]

manual_environments = {
    "butterfly/knights_archers_zombies",
    "butterfly/pistonball",
    "butterfly/cooperative_pong",
    "butterfly/prison",
    "butterfly/prospector",
    "sisl/pursuit"
}

all_environments = {
    "atari/basketball_pong": basketball_pong_v0,
    "atari/boxing": boxing_v0,
    "atari/combat_tank": combat_tank_v0,
    "atari/combat_plane": combat_plane_v0,
    "atari/double_dunk": double_dunk_v1,
    "atari/entombed_cooperative": entombed_cooperative_v0,
    "atari/entombed_competitive": entombed_competitive_v1,
    "atari/flag_capture": flag_capture_v0,
    "atari/foozpong": foozpong_v0,
    "atari/joust": joust_v1,
    "atari/ice_hockey": ice_hockey_v0,
    "atari/maze_craze": maze_craze_v1,
    "atari/mario_bros": mario_bros_v1,
    "atari/othello": othello_v1,
    "atari/pong": pong_v0,
    "atari/quadrapong": quadrapong_v1,
    "atari/space_invaders": space_invaders_v0,
    "atari/space_war": space_war_v0,
    "atari/surround": surround_v0,
    "atari/tennis": tennis_v1,
    "atari/video_checkers": video_checkers_v1,
    "atari/volleyball_pong": volleyball_pong_v0,
    "atari/wizard_of_wor": wizard_of_wor_v1,
    "atari/warlords": warlords_v1,

    "classic/chess": chess_v0,
    "classic/checkers": checkers_v0,
    "classic/rps": rps_v0,
    "classic/rpsls": rpsls_v0,
    "classic/connect_four": connect_four_v0,
    "classic/tictactoe": tictactoe_v0,
    "classic/leduc_holdem": leduc_holdem_v0,
    "classic/mahjong": mahjong_v0,
    "classic/texas_holdem": texas_holdem_v0,
    "classic/texas_holdem_no_limit": texas_holdem_no_limit_v0,
    "classic/uno": uno_v0,
    "classic/dou_dizhu": dou_dizhu_v0,
    "classic/gin_rummy": gin_rummy_v0,
    "classic/go": go_v0,
    "classic/hanabi": hanabi_v0,
    "classic/backgammon": backgammon_v0,

    "butterfly/knights_archers_zombies": knights_archers_zombies_v2,
    "butterfly/pistonball": pistonball_v0,
    "butterfly/cooperative_pong": cooperative_pong_v1,
    "butterfly/prison": prison_v1,
    "butterfly/prospector": prospector_v2,

    "magent/adversarial_pursuit": adversarial_pursuit_v1,
    "magent/battle": battle_v1,
    "magent/battlefield": battlefield_v1,
    "magent/combined_arms": combined_arms_v1,
    "magent/gather": gather_v1,
    "magent/tiger_deer": tiger_deer_v1,

    "mpe/simple_adversary": simple_adversary_v1,
    "mpe/simple_crypto": simple_crypto_v1,
    "mpe/simple_push": simple_push_v1,
    "mpe/simple_reference": simple_reference_v1,
    "mpe/simple_speaker_listener": simple_speaker_listener_v2,
    "mpe/simple_spread": simple_spread_v1,
    "mpe/simple_tag": simple_tag_v1,
    "mpe/simple_world_comm": simple_world_comm_v1,
    "mpe/simple": simple_v1,

    "sisl/multiwalker": multiwalker_v3,
    "sisl/waterworld": waterworld_v1,
    "sisl/pursuit": pursuit_v1,
}
