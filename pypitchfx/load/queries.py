'''
INSERT statements for populating the tables
'''
INSERT_PLAYERS = """
INSERT INTO player(
    player_id,
    full_name) 
VALUES(
    '{player_id}',
    '{full_name}');
 """
INSERT_GAME = """
INSERT INTO game(
    game_id,
    atbat,
    deck,
    hole,
    ind,
    innings_ids,
    url) 
VALUES(
    '{game_id}',
    '{at_bat}',
    '{deck}',
    '{hole}',
    '{ind}',
    ARRAY{innings_id},
    '{url}'
);
 """
INSERT_INNING = """
INSERT INTO inning(
    inning_id,num,
    away_team,
    home_team,
    next,
    top_inning_id,
    bottom_inning_id,
    game_id) 
VALUES(
    '{inning_id}',
    {num},
    '{away_team}',
    '{home_team}',
    {next},
    '{top_inning_id}',
    '{bottom_inning_id}',
    '{game_id}'
);"""
INSERT_HALF_INNING = """
INSERT INTO half_inning(
    half_inning_id,
    at_bats_actions_ids,
    inning_id) 
VALUES(
    '{half_inning_id}',
    ARRAY{at_bats_actions_id}::VARCHAR(36)[],
    '{inning_id}'
);"""
INSERT_ACTION="""
INSERT INTO action(
    action_id,
    b,
    s,
    o,
    des,
    event,
    tfs_zulu,
    player,
    pitch,
    event_num,
    home_team_runs,
    away_team_runs,
    half_inning_id) 
VALUES(
    '{action_id}',
    {b},
    {s},
    {o},
    '{des}',
    '{event}',
    '{tfs_zulu}',
    '{player}',
    {pitch},
    {event_num},
    {home_team_runs},
    {away_team_runs},
    '{half_inning_id}'
);"""
INSERT_AT_BAT="""
INSERT INTO at_bat(
    at_bat_id,
    num,
    b,
    s,
    o,
    start_tfs_zulu,
    batter,
    stand,
    b_height,
    pitcher,
    p_throws,
    des,
    event_num,
    event,
    home_team_runs,
    away_team_runs,
    score,
    pitch_ids,
    runner_ids,
    half_inning_id,
    outcome) 
VALUES(
    '{at_bat_id}',
    {num},
    {b},
    {s},
    {o},
    '{start_tfs_zulu}',
    '{batter}',
    '{stands}',
    {b_height},
    '{pitcher}',
    '{p_throws}',
    '{des}',
    {event_num},
    '{event}',
    {home_team_runs},
    {away_team_runs},
    {score},
    ARRAY{pitch_ids},
    ARRAY{runner_ids}::VARCHAR(36)[],
    '{half_inning_id}',
    {outcome}
);"""
INSERT_PITCH="""INSERT INTO pitch(
    pitch_id,
    des,
    id,
    type,
    tfs_zulu,
    x,
    y,
    event_num,
    sv_id,
    play_guid,
    start_speed,
    end_speed,
    sz_top,
    sz_bot,
    pfx_x,
    pfx_z,
    px,
    pz,
    x0,
    y0,
    z0,
    vx0,
    vy0,
    vz0,
    ax,
    ay,
    az,
    break_y,
    break_angle,
    pitch_type,
    type_confidence,
    zone,
    nasty,
    spin_dir,
    spin_rate,
    cc,
    mt,
    at_bat_id,
    outcome)
VALUES(
    '{pitch_id}',
    '{des}',
    {id},
    '{type}',
    '{tfs_zulu}',
    {x},
    {y},
    {event_num},
    '{sv_id}',
    '{play_guid}',
    {start_speed},
    {end_speed},
    {sz_top},
    {sz_bot},
    {pfx_x},
    {pfx_z},
    {px},
    {pz},
    {x0},
    {y0},
    {z0},
    {vx0},
    {vy0},
    {vz0},
    {ax},
    {ay},
    {az},
    {break_y},
    {break_angle},
    '{pitch_type}',
    {type_confidence},
    {zone},
    {nasty},
    {spin_dir},
    {spin_rate},
    '{cc}',
    '{mt}',
    '{at_bat_id}',
    {outcome}
);"""
INSERT_RUNNER="""
INSERT INTO runner(
    runner_id,
    id,
    start_base,
    end_base,
    event,
    score,
    rbi,
    earned,
    at_bat_id) 
VALUES(
    '{runner_id}',
    '{id}',
    {start},
    {end},
    '{event}',
    {score},
    {rbi},
    {earned},
    '{at_bat_id}'
);"""
INSERT_PICKOFF="""
INSERT INTO pickoff(
    po_id,
    des,
    event_num,
    at_bat_id) 
VALUES (
    '{po_id}',
    '{des}',
    {event_num},
    '{at_bat_id}'
);"""

#TODO: Finish impl
INSERT_GAMEPLAYER="""
INSERT INTO game_player(
id,
first,
last,
num,
boxname,
rl,
bats,
position,
status,
team_abbrev,
team_id,
parent_team_abbrev,
parent_team_id,
avg,
hr,
rbi,
current_position,
bat_order,
game_position,
wins,
losses,
era,
gid
)
VALUES
(
'{id}',
'{first}',
'{last}',
{num},
'{boxname}',
'{rl}',
'{bats}',
'{position}',
'{status}',
'{team_abbrev}',
'{team_id}',
'{parent_team_abbrev}',
'{parent_team_id}',
{avg},
{hr},
{rbi},
'{current_position}',
{bat_order},
'{game_position}',
{wins},
{losses},
{era},
'{gid}'
);
"""
