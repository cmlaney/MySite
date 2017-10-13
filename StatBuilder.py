
import sqlite3

connGame = sqlite3.connect("/home/cmlaney/mysite/games.sqlite")
cGame = connGame.cursor()

def buildStats(team):
    cGame.execute('select stat_3rd_down_att, stat_3rd_down_conv, off_yds, avg_yds_per_play, off_plays, \
                              stat_4th_down_att, stat_4th_down_conv, stat_1st_downs_total, stat_1st_downs_from_penalty,\
                              stat_1st_down_pass, stat_1st_down_rush, penalty_num, penalty_yards, int_recov_num, \
                              int_recov_yds, punt_ret_num, punt_ret_yds, pass_att, pass_comp, pass_yds_total, \
                              pass_yds_avg, pass_int_thrown, kick_ret_num, kick_ret_yds, rush_num, rush_yds_total, \
                              rush_yds_avg, fum_num, fum_lost, punt_num, punt_yds, start_date from team_stats \
                              join game on team_stats.game_id = game.id where team_name="{}" order by start_date'.format(team))

    stat_3rd_down_att = []
    stat_3rd_down_conv = []
    off_yds = []
    avg_yds_per_play = []
    off_plays = []
    stat_4th_down_att = []
    stat_4th_down_conv = []
    stat_1st_downs_total = []
    stat_1st_downs_from_penalty = []
    stat_1st_down_pass = []
    stat_1st_down_rush = []
    penalty_num = []
    penalty_yards = []
    int_recov_num = []
    int_recov_yds = []
    punt_ret_num = []
    punt_ret_yds = []
    pass_att = []
    pass_comp = []
    pass_yds_total = []
    pass_yds_avg = []
    pass_int_thrown = []
    kick_ret_num = []
    kick_ret_yds = []
    rush_num = []
    rush_yds_total = []
    rush_yds_avg = []
    fum_num = []
    fum_lost = []
    punt_num = []
    punt_yds = []
    date = []

    for row in cGame.fetchall():
        stat_3rd_down_att.append(row[0])
        stat_3rd_down_conv.append(row[1])
        off_yds.append(row[2])
        avg_yds_per_play.append(row[3])
        off_plays.append(row[4])
        stat_4th_down_att.append(row[5])
        stat_4th_down_conv.append(row[6])
        stat_1st_downs_total.append(row[7])
        stat_1st_downs_from_penalty.append(row[8])
        stat_1st_down_pass.append(row[9])
        stat_1st_down_rush.append(row[10])
        penalty_num.append(row[11])
        penalty_yards.append(row[12])
        int_recov_num.append(row[13])
        int_recov_yds.append(row[14])
        punt_ret_num.append(row[15])
        punt_ret_yds.append(row[16])
        pass_att.append(row[17])
        pass_comp.append(row[18])
        pass_yds_total.append(row[19])
        pass_yds_avg.append(row[20])
        pass_int_thrown.append(row[21])
        kick_ret_num.append(row[22])
        kick_ret_yds.append(row[23])
        rush_num.append(row[24])
        rush_yds_total.append(row[25])
        rush_yds_avg.append(row[26])
        fum_num.append(row[27])
        fum_lost.append(row[28])
        punt_num.append(row[29])
        punt_yds.append(row[30])
        date.append(row[31])



    stats = {
        'stat_3rd_down_att' : stat_3rd_down_att,
        'stat_3rd_down_conv': stat_3rd_down_conv,
        'off_yds': off_yds,
        'avg_yds_per_play': avg_yds_per_play,
        'off_plays': off_plays,
        'stat_4th_down_att': stat_4th_down_att,
        'stat_4th_down_conv': stat_4th_down_conv,
        'stat_1st_downs_total': stat_1st_downs_total,
        'stat_1st_downs_from_penalty': stat_1st_downs_from_penalty,
        'stat_1st_down_pass': stat_1st_down_pass,
        'stat_1st_down_rush': stat_1st_down_rush,
        'penalty_num': penalty_num,
        'penalty_yards': penalty_yards,
        'int_recov_num': int_recov_num,
        'int_recov_yds': int_recov_yds,
        'punt_ret_num': punt_ret_num,
        'punt_ret_yds': punt_ret_yds,
        'pass_att': pass_att,
        'pass_comp': pass_comp,
        'pass_yds_total': pass_yds_total,
        'pass_yds_avg': pass_yds_avg,
        'pass_int_thrown': pass_int_thrown,
        'kick_ret_num': kick_ret_num,
        'kick_ret_yds': kick_ret_yds,
        'rush_num': rush_num,
        'rush_yds_total': rush_yds_total,
        'rush_yds_avg': rush_yds_avg,
        'fum_num': fum_num,
        'fum_lost': fum_lost,
        'punt_num': punt_num,
        'punt_yds': punt_yds,
        'date': date
    }

    return stats

def getLastXGameAvg(stat, games=1):
    avg = 0;
    count = 0;
    while count <= games:
        pos = -1 * count
        avg += float(stat[pos])
        count += 1
    avg = avg/(count - 1)
    return avg

def getTeams():
    cGame.execute('select team_name, conference, division from team')
    teams = {}
    confs = ['ACC', 'B1G', 'Big XII', 'PAC-12', 'SEC', 'Independent', 'AAC', 'CUSA', 'MAC', 'MWC', 'Sun Belt']
    for conf in confs:
        teams[conf] = {}
    for row in cGame.fetchall():
        name = row[0]
        conf = row[1]
        div = row[2]
        if len(div) == 0:
            div = ' '
        if div not in teams[conf]:
            teams[conf][div] = []
        teams[conf][div].append(name)

    for conf, divs in teams.items():
        for div, confTeams in divs.items():
            teams[conf][div].sort()

    return teams

def getNiceKeys():

    stats = {
        'stat_3rd_down_att' : '3rd Down Attempts',
        'stat_3rd_down_conv': '3rd Down Conversions',
        'off_yds': 'Offensive Yards',
        'avg_yds_per_play': 'Avg Yards Per Play',
        'off_plays': 'Offensive Plays',
        'stat_4th_down_att': '4th Down Attempts',
        'stat_4th_down_conv': '4th Down Conversions',
        'stat_1st_downs_total': '1st Downs',
        'stat_1st_downs_from_penalty': 'Penalty 1st Downs',
        'stat_1st_down_pass': 'Passing 1st Downs',
        'stat_1st_down_rush': 'Rushing 1st Downs',
        'penalty_num': 'Penalties',
        'penalty_yards': 'Penalty Yards',
        'int_recov_num': 'Interceptions Recovered',
        'int_recov_yds': 'Interception Return Yards',
        'punt_ret_num': 'Punt Returns',
        'punt_ret_yds': 'Punt Return Yards',
        'pass_att': 'Pass Attempts',
        'pass_comp': 'Pass Completions',
        'pass_yds_total': 'Passing Yards',
        'pass_yds_avg': 'Avg Passing Yards',
        'pass_int_thrown': 'Interceptions Thrown',
        'kick_ret_num': 'Kick Returns',
        'kick_ret_yds': 'Kick Return Yards',
        'rush_num': 'Rush Attempts',
        'rush_yds_total': 'Rushing Yards',
        'rush_yds_avg': 'Avg Rushing Yards',
        'fum_num': 'Fumbles',
        'fum_lost': 'Fumbles Lost',
        'punt_num': 'Punts',
        'punt_yds': 'Punt Yards'
    }

    return stats
