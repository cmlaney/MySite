import json
import requests
from Game import Game, TeamInfo, TeamStats, Boxscore, Recap, Possession, Play, ScoringSummary, Score, PlayByPlay
import sqlite3

conn = sqlite3.connect("/home/cmlaney/mysite/games.sqlite")
c = conn.cursor()

def createDB():

    tn_team = 'team'

    c.execute('CREATE TABLE {} ({} {});'.format(tn_team, 'team_name', 'CHAR(100)'))

    tn_game = 'game'
    tn_game_cols_str = ['conference', 'start_date', 'location', \
                   'home_rank', 'home_iconURL', 'home_name', 'home_record', 'home_score', 'home_score_breakdown', \
                   'visiting_rank', 'visiting_iconURL', 'visiting_name', 'visiting_record', 'visiting_score', \
                   'visiting_score_breakdown', 'winner_name', 'recap_title', 'recap', 'game_url']

    c.execute('CREATE TABLE {} ({} {});'.format(tn_game, 'id', 'INTEGER PRIMARY KEY'))
    c.execute("ALTER TABLE {} ADD COLUMN '{}' {}".format(tn_game, 'start_time_epoch', 'INTEGER'))
    for col in tn_game_cols_str:
        c.execute("ALTER TABLE {} ADD COLUMN '{}' {}".format(tn_game, col, 'CHAR(1024)'))


    tn_stats = 'stats'

    c.execute('CREATE TABLE {} ({} {});'.format(tn_stats, 'id', 'INTEGER PRIMARY KEY'))
    c.execute("ALTER TABLE {} ADD COLUMN '{}' {}".format(tn_stats, 'game_id', 'INTEGER'))
    c.execute("ALTER TABLE {} ADD COLUMN '{}' {}".format(tn_stats, 'team_name', 'char(100)'))

    tn_stats_punt_ret_num = ['punt_ret_avg', 'punt_ret_yds', 'punt_ret_long', 'punt_ret_num']

    c.execute('CREATE TABLE {} ({} {});'.format('punt_return', 'stats_id', 'INTEGER'))
    c.execute("ALTER TABLE {} ADD COLUMN '{}' {}".format('punt_return', 'punt_ret_name', 'char(1024)'))
    for col in tn_stats_punt_ret_num:
        c.execute("ALTER TABLE {} ADD COLUMN '{}' {}".format('punt_return', col, 'REAL'))

    tn_stats_recv_num = ['recv_num', 'recv_td', 'recv_yds', 'recv_long']

    c.execute('CREATE TABLE {} ({} {});'.format('recv', 'stats_id', 'INTEGER'))
    c.execute("ALTER TABLE {} ADD COLUMN '{}' {}".format('recv', 'recv_name', 'char(1024)'))
    for col in tn_stats_recv_num:
        c.execute("ALTER TABLE {} ADD COLUMN '{}' {}".format('recv', col, 'REAL'))

    tn_stats_pass_num = ['pass_att', 'pass_comp', 'pass_int', 'pass_yds', 'pass_long', 'pass_td']

    c.execute('CREATE TABLE {} ({} {});'.format('pass', 'stats_id', 'INTEGER'))
    c.execute("ALTER TABLE {} ADD COLUMN '{}' {}".format('pass', 'pass_name', 'char(1024)'))
    for col in tn_stats_pass_num:
        c.execute("ALTER TABLE {} ADD COLUMN '{}' {}".format('pass', col, 'REAL'))

    tn_stats_rush_num = ['rush_num', 'rush_td', 'rush_yds', 'rush_long']

    c.execute('CREATE TABLE {} ({} {});'.format('rush', 'stats_id', 'INTEGER'))
    c.execute("ALTER TABLE {} ADD COLUMN '{}' {}".format('rush', 'rush_name', 'char(1024)'))
    for col in tn_stats_rush_num:
        c.execute("ALTER TABLE {} ADD COLUMN '{}' {}".format('rush', col, 'REAL'))

    tn_stats_kick_num = ['kick_fg', 'kick_fga', 'kick_xp', 'kick_pts', 'kick_long']

    c.execute('CREATE TABLE {} ({} {});'.format('kick', 'stats_id', 'INTEGER'))
    c.execute("ALTER TABLE {} ADD COLUMN '{}' {}".format('kick', 'kick_name', 'char(1024)'))
    for col in tn_stats_kick_num:
        c.execute("ALTER TABLE {} ADD COLUMN '{}' {}".format('kick', col, 'REAL'))

    tn_stats_punt_num = ['punt_avg', 'punt_long', 'punt_yds', 'punt_num']

    c.execute('CREATE TABLE {} ({} {});'.format('punt', 'stats_id', 'INTEGER'))
    c.execute("ALTER TABLE {} ADD COLUMN '{}' {}".format('punt', 'punt_name', 'char(1024)'))
    for col in tn_stats_punt_num:
        c.execute("ALTER TABLE {} ADD COLUMN '{}' {}".format('punt', col, 'REAL'))

    tn_stats_kick_ret_num = ['kick_ret_avg', 'kick_ret_yds', 'kick_ret_long', 'kick_ret_num']

    c.execute('CREATE TABLE {} ({} {});'.format('kick_ret', 'stats_id', 'INTEGER'))
    c.execute("ALTER TABLE {} ADD COLUMN '{}' {}".format('kick_ret', 'kick_ret_name', 'char(1024)'))
    for col in tn_stats_kick_ret_num:
        c.execute("ALTER TABLE {} ADD COLUMN '{}' {}".format('kick_ret', col, 'REAL'))

    tn_team_stats = 'team_stats'
    tn_team_stats_cols_num = ['stat_3rd_down_att', 'stat_3rd_down_conv', 'off_yds', 'avg_yds_per_play', 'off_plays', \
                              'stat_4th_down_att', 'stat_4th_down_conv', 'stat_1st_downs_total', \
                              'stat_1st_downs_from_penalty', 'stat_1st_down_pass', 'stat_1st_down_rush', \
                              'penalty_num', 'penalty_yards', 'int_recov_num', 'int_recov_yds', 'punt_ret_num', 'punt_ret_yds', \
                              'pass_att', 'pass_comp', 'pass_yds_total', 'pass_yds_avg', 'pass_int_thrown', 'kick_ret_num', \
                              'kick_ret_yds', 'rush_num', 'rush_yds_total', 'rush_yds_avg', 'fum_num', 'fum_lost', 'punt_num', \
                              'punt_yds']

    c.execute('CREATE TABLE {} ({} {});'.format(tn_team_stats, 'game_id', 'INTEGER'))
    c.execute("ALTER TABLE {} ADD COLUMN '{}' {}".format(tn_team_stats, 'team_name', 'char(100)'))
    for col in tn_team_stats_cols_num:
        c.execute("ALTER TABLE {} ADD COLUMN '{}' {}".format(tn_team_stats, col, 'REAL'))

    tn_possession = 'possession'
    tn_poss_cols_str = ['team_name', 'time', 'period']

    c.execute('CREATE TABLE {} ({} {});'.format(tn_possession, 'id', 'INTEGER PRIMARY KEY'))
    c.execute("ALTER TABLE {} ADD COLUMN '{}' {}".format(tn_possession, 'game_id', 'INTEGER'))
    for col in tn_poss_cols_str:
        c.execute("ALTER TABLE {} ADD COLUMN '{}' {}".format(tn_possession, col, 'CHAR(100)'))

    tn_play = 'play'
    tn_play_cols_str = ['text', 'drive']
    tn_play_cols_num = ['hScore', 'vScore']

    c.execute('CREATE TABLE {} ({} {});'.format(tn_play, 'possession_id', 'INTEGER'))
    for col in tn_play_cols_str:
        c.execute("ALTER TABLE {} ADD COLUMN '{}' {}".format(tn_play, col, 'CHAR(100)'))
    for col in tn_play_cols_num:
        c.execute("ALTER TABLE {} ADD COLUMN '{}' {}".format(tn_play, col, 'INTEGER'))

    tn_score = 'score'
    tn_score_cols_str = ['team_name', 'time', 'type', 'text', 'drive']
    tn_score_cols_num = ['vScore', 'hScore', 'period']

    c.execute('CREATE TABLE {} ({} {});'.format(tn_score, 'game_id', 'INTEGER'))
    for col in tn_score_cols_str:
        c.execute("ALTER TABLE {} ADD COLUMN '{}' {}".format(tn_score, col, 'CHAR(100)'))
    for col in tn_score_cols_num:
        c.execute("ALTER TABLE {} ADD COLUMN '{}' {}".format(tn_score, col, 'INTEGER'))

    c.execute("CREATE INDEX 'game_index' ON 'game' ('id' ASC);")
    c.execute("CREATE INDEX 'play_index' ON 'play' ('possession_id' ASC);")
    c.execute("CREATE INDEX 'poss_index' ON 'possession' ('game_id' ASC);")
    c.execute("CREATE INDEX 'score_index' ON 'score' ('game_id' ASC);")
    c.execute("CREATE INDEX 'stats_index' ON 'stats' ('game_id' ASC);")
    c.execute("CREATE INDEX 'team_stats_index' ON 'possession' ('game_id' ASC);")

def checkIfGameExists(url):
    c.execute('select * from game where game_url="{}"'.format(url))
    id_exists = c.fetchone()
    if id_exists:
        return True
    else:
        return False

def storeGame(game):

    recapTitle = ''
    recapText = ''
    if hasattr(game, 'recap'):
        recapTitle = game.recap.title
        recapText = game.recap.content


    c.execute('insert into game (start_time_epoch, conference, start_date, location, home_rank, home_iconURL, \
    home_name, home_record, home_score, home_score_breakdown, visiting_rank, visiting_iconURL, visiting_name, \
    visiting_record, visiting_score, visiting_score_breakdown, winner_name, recap_title, recap, game_url) values ({}, "{}", \
    "{}", "{}", "{}", "{}", "{}", "{}", "{}", "{}", "{}", "{}", "{}", "{}", "{}", "{}", "{}", "{}", "{}", "{}");'.format(\
        game.startTimeEpoch, game.conference, game.startDate, game.location, game.homeTeam.rank, game.homeTeam.iconURL, \
        game.homeTeam.nameRaw, game.homeTeam.record, game.homeTeam.currentScore, game.homeTeam.scoreBreakdown, \
        game.awayTeam.rank, game.awayTeam.iconURL, game.awayTeam.nameRaw, game.awayTeam.record, game.awayTeam.currentScore, \
        game.awayTeam.scoreBreakdown, game.winningTeam.nameRaw, recapTitle, recapText, game.url))
    last_game_id = c.lastrowid

    if hasattr(game, 'teamStats'):
        ts = game.teamStats
        for teamName, stats in ts.stats.iteritems():
            stat_3rd_down = stats['Third-Down Conversions']['data'].strip().replace('-', ' ').split()
            stat_3rd_down_conv = float(stat_3rd_down[0])
            stat_3rd_down_att = float(stat_3rd_down[1])

            stat_off_yds = float(stats['Total Offense']['data'])
            stat_avg_yds_per_play = float(stats['Total Offense']['breakdown']['Avg. Per Play'].replace('-', '0'))
            stat_off_plays = int(stats['Total Offense']['breakdown']['Plays'])

            stat_4th_down = stats['Fourth-Down Conversions']['data'].strip().replace('-', ' ').split()
            stat_4th_down_conv = int(stat_4th_down[0])
            stat_4th_down_att = int(stat_4th_down[1])

            stat_1st_downs = int(stats['1st Downs']['data'])
            stat_1st_downs_pen = int(stats['1st Downs']['breakdown']['Penalty'])
            stat_1st_downs_pass = int(stats['1st Downs']['breakdown']['Passing'])
            stat_1st_downs_rush = int(stats['1st Downs']['breakdown']['Rushing'])

            stat_penalties = (stats['Penalties: Number-Yards']['data']).strip().replace('-', ' ').split()
            stat_pen_num = int(stat_penalties[0])
            stat_pen_yds = float(stat_penalties[1])

            stat_int_rets = (stats['Interception Returns: Number-Yards']['data']).strip().replace('-', ' ').split()
            stat_int_rets_num = int(stat_int_rets[0])
            stat_int_rets_yds = float(stat_int_rets[1])

            stat_punt_ret = (stats['Punt Returns: Number-Yards']['data']).strip().replace('-', ' ').split()
            stat_punt_ret_num = int(stat_punt_ret[0])
            stat_punt_ret_yds = float(stat_punt_ret[1])

            stat_passing_yds = float(stats['Passing']['data'])
            stat_passing_att = int(stats['Passing']['breakdown']['Attempts'])
            stat_passing_avg = float(stats['Passing']['breakdown']['Avg. Per Pass'].replace('-', '0'))
            stat_passing_int = int(stats['Passing']['breakdown']['Interceptions'])
            stat_passing_comp = int(stats['Passing']['breakdown']['Completions'])

            stat_rush_yds = float(stats['Rushing']['data'])
            stat_rush_att = int(stats['Rushing']['breakdown']['Attempts'])
            stat_rush_avg = float(stats['Rushing']['breakdown']['Avg. Per Rush'].replace('-', '0'))

            stat_kick_ret = (stats['Kickoff Returns: Number-Yards']['data']).strip().replace('-', ' ').split()
            stat_kick_ret_num = int(stat_kick_ret[0])
            stat_kick_ret_yds = float(stat_kick_ret[1])

            stat_fum = (stats['Fumbles: Number-Lost']['data']).strip().replace('-', ' ').split()
            stat_fum_num = int(stat_fum[0])
            stat_fum_lost = int(stat_fum[1])

            stat_punt = (stats['Punting: Number-Yards']['data']).strip().replace('-', ' ').split()
            stat_punt_num = 0
            stat_punt_yds = 0
            if len(stat_punt) == 2:
                stat_punt_num = int(stat_punt[0])
                stat_punt_yds = float(stat_punt[1])

            c.execute('insert into team_stats (game_id, team_name, stat_3rd_down_att, stat_3rd_down_conv, off_yds, avg_yds_per_play, \
            off_plays, stat_4th_down_att, stat_4th_down_conv, stat_1st_downs_total, stat_1st_downs_from_penalty, \
            stat_1st_down_pass, stat_1st_down_rush, \
            penalty_num, penalty_yards, int_recov_num, int_recov_yds, punt_ret_num, punt_ret_yds, pass_att, pass_comp, \
            pass_yds_total, pass_yds_avg, pass_int_thrown, kick_ret_num, kick_ret_yds, rush_num, rush_yds_total, rush_yds_avg, \
            fum_num, fum_lost, punt_num, punt_yds) values ({}, "{}", {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, \
            {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {})'.format(last_game_id, teamName, stat_3rd_down_att, \
                                                        stat_3rd_down_conv, stat_off_yds, stat_avg_yds_per_play, stat_off_plays, \
                                                                                        stat_4th_down_att, stat_4th_down_conv, \
                                                        stat_1st_downs, stat_1st_downs_pen, stat_1st_downs_pass, stat_1st_downs_rush, \
                                                        stat_pen_num, stat_pen_yds, stat_int_rets_num, stat_int_rets_yds, \
                                                        stat_punt_ret_num, stat_punt_ret_yds, stat_passing_att, stat_passing_comp, \
                                                        stat_passing_yds, stat_passing_avg, stat_passing_int, stat_kick_ret_num, \
                                                        stat_kick_ret_yds, stat_rush_att, stat_rush_yds, stat_rush_avg, stat_fum_num, \
                                                        stat_fum_lost, stat_punt_num, stat_punt_yds))

    if hasattr(game, 'boxscore'):
        team_name_visit = game.awayTeam.nameRaw
        c.execute('insert into stats (game_id, team_name) values ({}, "{}")'.format(last_game_id, team_name_visit))
        stats_id =  c.lastrowid
        punt_ret_visit = game.boxscore.tables['punt_returns_visiting']
        for name, punt_ret in punt_ret_visit.iteritems():
            punt_ret['AVG'] = punt_ret['AVG'].replace('-', '0')
            if len(punt_ret['LONG']) == 0:
                punt_ret['LONG'] = '0'
            c.execute('insert into punt_return (stats_id, punt_ret_name, punt_ret_avg, punt_ret_yds, punt_ret_long, \
            punt_ret_num) values ({}, "{}", {}, {}, {}, {})'.format(stats_id, punt_ret['PUNT RETURNS'], \
                    float(punt_ret['AVG']), float(punt_ret['YDS']), float(punt_ret['LONG']), float(punt_ret['NO'])))

        passing_visit = game.boxscore.tables['passing_visiting']
        for name, passing in passing_visit.iteritems():
            pass_att = passing['CP-ATT-INT'].strip().split('-')
            if len(passing['LONG']) == 0:
                passing['LONG'] = '0'
            c.execute('insert into pass (stats_id, pass_name, pass_att, pass_comp, pass_int, pass_yds, pass_td, \
            pass_long) values ({}, "{}", {}, {}, {}, {}, {}, {})'.format(stats_id, passing['PASSING'], float(pass_att[1]), \
                    float(pass_att[0]), float(pass_att[2]), float(passing['YDS']), float(passing['TD']), float(passing['LONG'])))

        receiving_visit = game.boxscore.tables['receiving_visiting']
        for name, recv in receiving_visit.iteritems():
            if len(recv['LONG']) == 0:
                recv['LONG'] = '0'
            c.execute('insert into recv (stats_id, recv_name, recv_num, recv_td, recv_yds, recv_long) \
            values ({}, "{}", {}, {}, {}, {})'.format(stats_id, recv['RECEIVING'], float(recv['REC']), \
                    float(recv['TD']), float(recv['YDS']), float(recv['LONG'])))

        kicking_visit = game.boxscore.tables['kicking_visiting']
        for name, kick in kicking_visit.iteritems():
            if len(kick['LONG'].replace('-', '')) == 0:
                kick['LONG'] = '0'
            fg_stat = kick['FG-FGA'].strip().split('/')
            c.execute('insert into kick (stats_id, kick_name, kick_fg, kick_fga, kick_xp, kick_pts, kick_long) \
            values ({}, "{}", {}, {}, {}, {}, {})'.format(stats_id, kick['KICKING'], float(fg_stat[0]), \
                        float(fg_stat[1]), float(kick['XP']), float(kick['PTS']), float(kick['LONG'])))

        punting_visit = game.boxscore.tables['punting_visiting']
        for name, punt in punting_visit.iteritems():
            punt['AVG'] = punt['AVG'].replace('-', '0')
            punt['LONG'] = punt['LONG'].replace('-', '0')
            if len(punt['LONG']) == 0:
                punt['LONG'] = '0'
            if len(punt['AVG']) == 0:
                punt['AVG'] = '0'
            if len(punt['YDS']) == 0:
                punt['YDS'] = '0'
            if len(punt['NO']) == 0:
                punt['NO'] = '0'
            if len(punt['LONG'].replace('-', '')) == 0:
                punt['LONG'] = '0'
            if len(punt['AVG'].replace('-', '')) == 0:
                punt['AVG'] = '0'
            c.execute('insert into punt (stats_id, punt_name, punt_avg, punt_long, punt_yds, punt_num) \
            values ({}, "{}", {}, {}, {}, {})'.format(stats_id, punt['PUNTING'], float(punt['AVG']), \
                                                      float(punt['LONG']), float(punt['YDS']), float(punt['NO'])))

        rushing_visit = game.boxscore.tables['rushing_visiting']
        for name, rush in rushing_visit.iteritems():
            if len(rush['LONG']) == 0:
                rush['LONG'] = '0'
            c.execute('insert into rush (stats_id, rush_name, rush_num, rush_td, rush_yds, rush_long) \
            values ({}, "{}", {}, {}, {}, {})'.format(stats_id, rush['RUSHING'], float(rush['ATT']), \
                                                      float(rush['TD']), float(rush['YDS']), float(rush['LONG'])))

        kick_returns_visit = game.boxscore.tables['kick_returns_visiting']
        for name, kick_ret in kick_returns_visit.iteritems():
            kick_ret['AVG'] = kick_ret['AVG'].replace('-', '0')
            kick_ret['LONG'] = kick_ret['LONG'].replace('-', '0')
            if len(kick_ret['LONG']) == 0:
                kick_ret['LONG'] = '0'
            if len(kick_ret['AVG']) == 0:
                kick_ret['AVG'] = '0'
            if len(kick_ret['YDS']) == 0:
                kick_ret['YDS'] = '0'
            if len(kick_ret['NO']) == 0:
                kick_ret['NO'] = '0'
            c.execute('insert into kick_ret (stats_id, kick_ret_name, kick_ret_avg, kick_ret_yds, kick_ret_long, \
            kick_ret_num) values ({}, "{}", {}, {}, {}, {})'.format(stats_id, kick_ret['KICK RETURNS'], \
                    float(kick_ret['AVG']), float(kick_ret['YDS']), float(kick_ret['LONG']), float(kick_ret['NO'])))

        team_name_home = game.homeTeam.nameRaw
        c.execute('insert into stats (game_id, team_name) values ({}, "{}")'.format(last_game_id, team_name_home))
        stats_id = c.lastrowid
        punt_ret_home = game.boxscore.tables['punt_returns_home']
        for name, punt_ret in punt_ret_home.iteritems():
            punt_ret['AVG'] = punt_ret['AVG'].replace('-', '0')
            if len(punt_ret['LONG']) == 0:
                punt_ret['LONG'] = '0'
            c.execute('insert into punt_return (stats_id, punt_ret_name, punt_ret_avg, punt_ret_yds, punt_ret_long, \
                    punt_ret_num) values ({}, "{}", {}, {}, {}, {})'.format(stats_id, punt_ret['PUNT RETURNS'], \
                                                                             float(punt_ret['AVG']),
                                                                             float(punt_ret['YDS']),
                                                                             float(punt_ret['LONG']),
                                                                             float(punt_ret['NO'])))

        passing_home = game.boxscore.tables['passing_home']
        for name, passing in passing_home.iteritems():
            pass_att = passing['CP-ATT-INT'].strip().split('-')
            if len(passing['LONG']) == 0:
                passing['LONG'] = '0'
            c.execute('insert into pass (stats_id, pass_name, pass_att, pass_comp, pass_int, pass_yds, pass_td, \
                    pass_long) values ({}, "{}", {}, {}, {}, {}, {}, {})'.format(stats_id, passing['PASSING'],
                                                                                  float(pass_att[1]), \
                                                                                  float(pass_att[0]),
                                                                                  float(pass_att[2]),
                                                                                  float(passing['YDS']),
                                                                                  float(passing['TD']),
                                                                                  float(passing['LONG'])))

        receiving_home = game.boxscore.tables['receiving_home']
        for name, recv in receiving_home.iteritems():
            if len(recv['LONG']) == 0:
                recv['LONG'] = '0'
            c.execute('insert into recv (stats_id, recv_name, recv_num, recv_td, recv_yds, recv_long) \
                    values ({}, "{}", {}, {}, {}, {})'.format(stats_id, recv['RECEIVING'], float(recv['REC']), \
                                                              float(recv['TD']), float(recv['YDS']),
                                                              float(recv['LONG'])))

        kicking_home = game.boxscore.tables['kicking_home']
        for name, kick in kicking_home.iteritems():
            if len(kick['LONG'].replace('-', '')) == 0:
                kick['LONG'] = '0'
            if len(kick['PTS'].replace('-', '')) == 0:
                kick['PTS'] = '0'
            fg_stat = kick['FG-FGA'].strip().split('/')
            c.execute('insert into kick (stats_id, kick_name, kick_fg, kick_fga, kick_xp, kick_pts, kick_long) \
                    values ({}, "{}", {}, {}, {}, {}, {})'.format(stats_id, kick['KICKING'], float(fg_stat[0]), \
                                                                  float(fg_stat[1]), float(kick['XP']),
                                                                  float(kick['PTS']), float(kick['LONG'])))

        punting_home = game.boxscore.tables['punting_home']
        for name, punt in punting_home.iteritems():
            punt['AVG'] = punt['AVG'].replace('-', '0')
            punt['LONG'] = punt['LONG'].replace('-', '0')
            if len(punt['LONG']) == 0:
                punt['LONG'] = '0'
            if len(punt['AVG']) == 0:
                punt['AVG'] = '0'
            if len(punt['YDS']) == 0:
                punt['YDS'] = '0'
            if len(punt['NO']) == 0:
                punt['NO'] = '0'
            c.execute('insert into punt (stats_id, punt_name, punt_avg, punt_long, punt_yds, punt_num) \
                    values ({}, "{}", {}, {}, {}, {})'.format(stats_id, punt['PUNTING'], float(punt['AVG']), \
                                                              float(punt['LONG']), float(punt['YDS']),
                                                              float(punt['NO'])))

        rushing_home = game.boxscore.tables['rushing_home']
        for name, rush in rushing_home.iteritems():
            if len(rush['LONG']) == 0:
                rush['LONG'] = '0'
            c.execute('insert into rush (stats_id, rush_name, rush_num, rush_td, rush_yds, rush_long) \
                    values ({}, "{}", {}, {}, {}, {})'.format(stats_id, rush['RUSHING'], float(rush['ATT']), \
                                                              float(rush['TD']), float(rush['YDS']),
                                                              float(rush['LONG'])))

        kick_returns_home = game.boxscore.tables['kick_returns_home']
        for name, kick_ret in kick_returns_home.iteritems():
            kick_ret['AVG'] = kick_ret['AVG'].replace('-', '0')
            kick_ret['LONG'] = kick_ret['LONG'].replace('-', '0')
            if len(kick_ret['LONG']) == 0:
                kick_ret['LONG'] = '0'
            if len(kick_ret['AVG']) == 0:
                kick_ret['AVG'] = '0'
            if len(kick_ret['YDS']) == 0:
                kick_ret['YDS'] = '0'
            if len(kick_ret['NO']) == 0:
                kick_ret['NO'] = '0'
            c.execute('insert into kick_ret (stats_id, kick_ret_name, kick_ret_avg, kick_ret_yds, kick_ret_long, \
                    kick_ret_num) values ({}, "{}", {}, {}, {}, {})'.format(stats_id, kick_ret['KICK RETURNS'], \
                                                                             float(kick_ret['AVG'].replace('-', '0')),
                                                                             float(kick_ret['YDS']),
                                                                             float(kick_ret['LONG']),
                                                                             float(kick_ret['NO'])))

    if hasattr(game, 'scoringSummary'):
        for period, scores in game.scoringSummary.periods.iteritems():
            period_int = getPeriodInt(period)
            for score in scores:
                c.execute('insert into score (game_id, team_name, period, time, type, text, drive, vScore, hScore) \
                values ({}, "{}", {}, "{}", "{}", "{}", "{}", {}, {})'.format(last_game_id, score.teamName, period_int, \
                                                                                score.time, score.type, score.text, score.drive, \
                                                                                int(score.visitorScore), int(score.homeScore)))

    if hasattr(game, 'playByPlay'):
        for period, possessions in game.playByPlay.periods.iteritems():
            period_int = getPeriodInt(period)
            for possession in possessions:
                c.execute('insert into possession (game_id, team_name, time, period) values ({}, "{}", "{}", {})'\
                          .format(last_game_id, possession.teamName, possession.time, period_int))
                possession_id = c.lastrowid
                for play in possession.plays:
                    c.execute('insert into play (possession_id, text, drive, hScore, vScore) values ({}, "{}", "{}", {}, {})'\
                              .format(possession_id, play.text, play.drive, play.hScore, play.vScore))

def getPeriodInt(period):
    period_int = -1
    if 'OT' in period:
        period_int = 5
    elif '2OT' in period:
        period_int = 6
    elif '3OT' in period:
        period_int = 7
    elif '4OT' in period:
        period_int = 8
    elif '5OT' in period:
        period_int = 9
    elif '6OT' in period:
        period_int = 10
    elif '7OT' in period:
        period_int = 11
    elif '8OT' in period:
        period_int = 12
    elif '9OT' in period:
        period_int = 13
    elif '10OT' in period:
        period_int = 14
    elif '1' in period:
        period_int = 1
    elif '2' in period:
        period_int = 2
    elif '3' in period:
        period_int = 3
    elif '4' in period:
        period_int = 4
    return period_int

def fetchGames(week, refetch=False, store=False):
    url = 'http://data.ncaa.com/sites/default/files/data/scoreboard/football/fbs/2017/{}/scoreboard.json'.format(week)
    data = requests.get(url=url)
    output = json.loads(data.content)
    games = {}

    for group in output['scoreboard']:
        print(group['day'])
        for game in group['games']:
            key, newGame = fetchSpecific(game, refetch)
            if len(key) > 0:
                games[key] = newGame
                if store:
                    print('Storing: {}'.format(key))
                    storeGame(newGame)
                    conn.commit()
    return games

def fetchSpecific(game, refetch = False):
    exists = checkIfGameExists(game)
    if not exists or refetch:
        gameUrl = 'http://data.ncaa.com' + str(game)
        gameResp = requests.get(url=gameUrl)
        gameData = json.loads(gameResp.content)
        if 'gameStatus' not in gameData:
            gameData['gameStatus'] = ''
        if 'periodStatus' not in gameData:
            gameData['periodStatus'] = ''
        if 'downToGo' not in gameData:
            gameData['downToGo'] = ''
        if 'finalMessage' not in gameData:
            gameData['finalMessage'] = ''
        if 'currentPeriod' not in gameData:
            gameData['currentPeriod'] = ''
        newGame = Game(gameData['id'], gameData['conference'], gameData['updatedTimestamp'], gameData['gameState'], \
                       gameData['startDate'], gameData['startTimeEpoch'], gameData['currentPeriod'], \
                       gameData['finalMessage'], gameData['gameStatus'], gameData['periodStatus'], \
                       gameData['downToGo'], gameData['timeclock'], gameData['location'], \
                       gameData['scoreBreakdown'], gameData['home'], gameData['away'], gameData['tabsArray'], game)
        key = 'Home: {} - Away: {} - Date: {}'.format(newGame.homeTeam.nameRaw, newGame.awayTeam.nameRaw,
                                                      newGame.startDate)
        print('Fetched: {}'.format(key))
        return key, newGame
    else:
        print('Game exists in DB and refetch not specified: {}'.format(game))
        return '', False

def populate(weeks):
    for week in weeks:
        games = fetchGames(week=week, store=True)
        for key, game in games.iteritems():
            print('Storing: {}'.format(key))
            #storeGame(game)
    conn.commit()
    conn.close()



