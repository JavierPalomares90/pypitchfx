'''
SQL statements for creating
and populating the tables
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
    url,
    gid) 
VALUES(
    '{game_id}',
    '{at_bat}',
    '{deck}',
    '{hole}',
    '{ind}',
    ARRAY{innings_id},
    '{url}',
    '{gid}'
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
    isTop,
    game_id,
    inning_id)
VALUES(
    '{half_inning_id}',
    ARRAY{at_bats_actions_id}::VARCHAR(36)[],
    {isTop},
    '{game_id}',
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
    game_id,
    inning_id,
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
    '{game_id}',
    '{inning_id}',
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
    game_id,
    inning_id,
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
    '{game_id}',
    '{inning_id}',
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
    break_length,
    pitch_type,
    type_confidence,
    zone,
    nasty,
    spin_dir,
    spin_rate,
    cc,
    mt,
    game_id,
    inning_id,
    half_inning_id,
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
    {break_length},
    '{pitch_type}',
    {type_confidence},
    {zone},
    {nasty},
    {spin_dir},
    {spin_rate},
    '{cc}',
    '{mt}',
    '{game_id}',
    '{inning_id}',
    '{half_inning_id}',
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
    game_id,
    inning_id,
    half_inning_id,
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
    '{game_id}',
    '{inning_id}',
    '{half_inning_id}',
    '{at_bat_id}'
);"""

INSERT_PICKOFF="""
INSERT INTO pickoff(
    po_id,
    des,
    event_num,
    game_id,
    inning_id,
    half_inning_id,
    at_bat_id)
VALUES (
    '{po_id}',
    '{des}',
    {event_num},
    '{game_id}',
    '{inning_id}',
    '{half_inning_id}',
    '{at_bat_id}'
);"""

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
    gid)
VALUES(
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

CREATE_GAME_TABLE="""
CREATE TABLE game(
    game_id VARCHAR(36) PRIMARY KEY,
    atBat VARCHAR (6)  NOT NULL,
    deck VARCHAR (6) NOT NULL,
    hole VARCHAR (6),
    ind TEXT,
    innings_ids VARCHAR(36)[] NOT NULL,
    url TEXT,
    gid TEXT UNIQUE);
"""

CREATE_INNING_TABLE="""
CREATE TABLE inning(
    inning_id VARCHAR(36) PRIMARY KEY,
    num INTEGER NOT NULL,
    away_team VARCHAR(50) NOT NULL,
    home_team VARCHAR(5) NOT NULL,
    next BOOLEAN NOT NULL,
    top_inning_id VARCHAR(36) NOT NULL,
    bottom_inning_id VARCHAR(36),
    game_id VARCHAR(36) NOT NULL,
    FOREIGN KEY (game_id) REFERENCES game(game_id) ON DELETE CASCADE);
"""

CREATE_HALF_INNING_TABLE="""
CREATE TABLE half_inning(
    half_inning_id VARCHAR(36) PRIMARY KEY,
    at_bats_actions_ids VARCHAR(36)[] NOT NULL,
    isTop BOOLEAN NOT NULL,
    game_id VARCHAR(36) NOT NULL,
    inning_id VARCHAR(36) NOT NULL,
    FOREIGN KEY (inning_id) REFERENCES inning(inning_id) ON DELETE CASCADE);
"""

CREATE_AT_BAT_TABLE="""
CREATE TABLE at_bat(
    at_bat_id VARCHAR(36) PRIMARY KEY,
    num INTEGER NOT NULL,
    b INTEGER NOT NULL,
    o INTEGER NOT NULL,
    start_tfs_zulu TIMESTAMP,
    batter VARCHAR(6) NOT NULL,
    stand VARCHAR(1),
    b_height INTEGER,
    pitcher VARCHAR(6) NOT NULL,
    p_throws VARCHAR(1),
    des TEXT,
    event_num INTEGER NOT NULL,
    event TEXT,
    home_team_runs INTEGER NOT NULL,
    away_team_runs INTEGER NOT NULL,
    score BOOLEAN,
    pitch_ids VARCHAR(36)[] NOT NULL,
    runner_ids VARCHAR(36)[],
    outcome NUMERIC NOT NULL,
    s INTEGER,
    game_id VARCHAR(36) NOT NULL,
    inning_id VARCHAR(36) NOT NULL,
    half_inning_id VARCHAR(36),
    FOREIGN KEY (half_inning_id) REFERENCES half_inning(half_inning_id) ON DELETE CASCADE
    );
"""

CREATE_PITCH_TABLE="""
CREATE TABLE pitch( 
    pitch_id VARCHAR(36) PRIMARY KEY,
    des TEXT, 
    id INTEGER,
    type VARCHAR(10), 
    tfs_zulu TIMESTAMP,
    x NUMERIC, 
    y NUMERIC,
    event_num INTEGER, 
    sv_id VARCHAR(13),
    play_guid VARCHAR(50), 
    start_speed NUMERIC,
    end_speed NUMERIC, 
    sz_top NUMERIC,
    sz_bot NUMERIC, 
    pfx_x NUMERIC,
    pfx_z NUMERIC, 
    px NUMERIC,
    pz NUMERIC, 
    x0 NUMERIC,
    y0 NUMERIC, 
    z0 NUMERIC,
    vx0 NUMERIC, 
    vy0 NUMERIC,
    vz0 NUMERIC, 
    ax NUMERIC,
    ay NUMERIC, 
    az NUMERIC,
    break_y NUMERIC, 
    break_angle NUMERIC,
    break_length NUMERIC, 
    pitch_type VARCHAR(10),
    type_confidence NUMERIC, 
    zone INTEGER,
    nasty INTEGER, 
    spin_dir NUMERIC,
    spin_rate NUMERIC, 
    cc  VARCHAR(10),
    mt  VARCHAR(10), 
    outcome NUMERIC,
    game_id VARCHAR(36) NOT NULL,
    inning_id VARCHAR(36) NOT NULL, 
    half_inning_id VARCHAR(36),
    at_bat_id VARCHAR(36) NOT NULL,
    FOREIGN KEY (at_bat_id) REFERENCES at_bat(at_bat_id) ON DELETE CASCADE);
"""

CREATE_RUNNER_TABLE="""
CREATE TABLE runner( 
    runner_id VARCHAR(36) PRIMARY KEY, 
    id VARCHAR(6) NOT NULL, 
    start_base INTEGER NOT NULL, 
    end_base INTEGER, 
    event TEXT, 
    score BOOLEAN, 
    rbi BOOLEAN, 
    earned BOOLEAN, 
    game_id VARCHAR(36) NOT NULL,
    inning_id VARCHAR(36) NOT NULL, 
    half_inning_id VARCHAR(36),
    at_bat_id VARCHAR(36) NOT NULL,
    FOREIGN KEY (at_bat_id) REFERENCES at_bat(at_bat_id) ON DELETE CASCADE);
"""

CREATE_PICKOFF_TABLE="""
CREATE TABLE pickoff(
    po_id VARCHAR(36) PRIMARY KEY,
    des TEXT,
    event_num INTEGER,
    game_id VARCHAR(36) NOT NULL,
    inning_id VARCHAR(36) NOT NULL, 
    half_inning_id VARCHAR(36),
    at_bat_id VARCHAR(36) NOT NULL,
    FOREIGN KEY (at_bat_id) REFERENCES at_bat(at_bat_id) ON DELETE CASCADE);
"""

CREATE_ACTION_TABLE="""
CREATE TABLE action( 
    action_id VARCHAR(36) PRIMARY KEY, 
    b INTEGER, 
    s INTEGER, 
    o INTEGER, 
    des TEXT, 
    event TEXT, 
    tfs_zulu TIMESTAMP, 
    player VARCHAR(6), 
    pitch INTEGER, 
    event_num INTEGER, 
    home_team_runs INTEGER, 
    away_team_runs INTEGER, 
    game_id VARCHAR(36) NOT NULL,
    inning_id VARCHAR(36) NOT NULL, 
    half_inning_id VARCHAR(36),
    FOREIGN KEY (half_inning_id) REFERENCES half_inning(half_inning_id) ON DELETE CASCADE);
"""

CREATE_GAME_PLAYER_TABLE="""
CREATE TABLE game_player( 
    id VARCHAR(36), 
    first TEXT, 
    last TEXT, 
    num INTEGER, 
    boxname TEXT, 
    rl TEXT, 
    bats TEXT, 
    position TEXT, 
    status TEXT, 
    team_abbrev TEXT, 
    team_id TEXT, 
    parent_team_abbrev TEXT, 
    parent_team_id TEXT, 
    avg NUMERIC, 
    hr INTEGER, 
    rbi INTEGER, 
    current_position TEXT, 
    bat_order INTEGER, 
    game_position TEXT, 
    wins INTEGER, 
    losses INTEGER, 
    era NUMERIC, 
    gid TEXT,
    PRIMARY KEY(id,gid),
    FOREIGN KEY (gid) REFERENCES game(gid) ON DELETE CASCADE
); 
"""

