
import operator
from datetime import datetime

class Analyzer():

    def __init__(self):
        self.teams = {}
        self.schedules = {}
        self.init_dictionary()
        self.import_schedules()
        self.import_total_off()
        self.import_total_def()
        self.import_passing_off()
        self.import_passing_def()
        self.import_rushing_off()
        self.import_rushing_def()
        self.import_spteams_punting()
        self.import_spteams_returning()

    def init_dictionary(self):
        file = open("/home/cmlaney/mysite/ncaa_stats/teams.txt")
        for line in file:
            self.teams[line.strip()] = {}
            self.schedules[line.strip()] = {}

    def import_schedules(self):
        file = open("/home/cmlaney/mysite/ncaa_stats/schedule.csv")
        first = True
        keys = {}
        for line in file:
            split = line.strip().split(",")
            if first:
                keys = split
                first = False
            else:
                schedule = {}
                values = dict(zip(keys, split))
                opponent = values['OPPONENT_NAME']
                schedule['date'] = values['GAME_DATE']
                schedule['location'] = values['LOC']
                self.schedules[values['ORG_NAME']][opponent] = schedule

    def import_total_off(self):
        file = open("/home/cmlaney/mysite/ncaa_stats/total_offense.csv")
        first = True
        counter = 1
        keys = {}
        for line in file:
            split = line.strip().split(",")
            split = list(filter(None, split))
            if first:
                keys = split[1:]
                first = False
            else:
                self.teams[split[0]]["total_offense"] = dict(zip(keys, split[1:]))
                self.teams[split[0]]["total_offense_rank"] = counter
                counter += 1

    def import_total_def(self):
        file = open("/home/cmlaney/mysite/ncaa_stats/total_defense.csv")
        first = True
        counter = 1
        keys = {}
        for line in file:
            split = line.strip().split(",")
            split = list(filter(None, split))
            if first:
                keys = split[1:]
                first = False
            else:
                self.teams[split[0]]["total_defense"] = dict(zip(keys, split[1:]))
                self.teams[split[0]]["total_defense_rank"] = counter
                counter += 1

    def import_passing_off(self):
        file = open("/home/cmlaney/mysite/ncaa_stats/passing_offense.csv")
        first = True
        counter = 1
        keys = {}
        for line in file:
            split = line.strip().split(",")
            split = list(filter(None, split))
            if first:
                keys = split[1:]
                first = False
            else:
                self.teams[split[0]]["passing_offense"] = dict(zip(keys, split[1:]))
                self.teams[split[0]]["passing_offense_rank"] = counter
                counter += 1

    def import_passing_def(self):
        file = open("/home/cmlaney/mysite/ncaa_stats/passing_defense.csv")
        first = True
        counter = 1
        keys = {}
        for line in file:
            split = line.strip().split(",")
            split = list(filter(None, split))
            if first:
                keys = split[1:]
                first = False
            else:
                self.teams[split[0]]["passing_defense"] = dict(zip(keys, split[1:]))
                self.teams[split[0]]["passing_defense_rank"] = counter
                counter += 1

    def import_rushing_off(self):
        file = open("/home/cmlaney/mysite/ncaa_stats/rushing_offense.csv")
        first = True
        counter = 1
        keys = {}
        for line in file:
            split = line.strip().split(",")
            split = list(filter(None, split))
            if first:
                keys = split[1:]
                first = False
            else:
                self.teams[split[0]]["rushing_offense"] = dict(zip(keys, split[1:]))
                self.teams[split[0]]["rushing_offense_rank"] = counter
                counter += 1

    def import_rushing_def(self):
        file = open("/home/cmlaney/mysite/ncaa_stats/rushing_defense.csv")
        first = True
        counter = 1
        keys = {}
        for line in file:
            split = line.strip().split(",")
            split = list(filter(None, split))
            if first:
                keys = split[1:]
                first = False
            else:
                self.teams[split[0]]["rushing_defense"] = dict(zip(keys, split[1:]))
                self.teams[split[0]]["rushing_defense_rank"] = counter
                counter += 1

    def import_spteams_punting(self):
        file = open("/home/cmlaney/mysite/ncaa_stats/spteams_punting.csv")
        first = True
        counter = 1
        keys = {}
        for line in file:
            split = line.strip().split(",")
            split = list(filter(None, split))
            if first:
                keys = split[1:]
                first = False
            else:
                self.teams[split[0]]["spteams_punting"] = dict(zip(keys, split[1:]))
                self.teams[split[0]]["spteams_punting_rank"] = counter
                counter += 1

    def import_spteams_returning(self):
        file = open("/home/cmlaney/mysite/ncaa_stats/spteams_returning.csv")
        first = True
        counter = 1
        keys = {}
        for line in file:
            split = line.strip().split(",")
            split = list(filter(None, split))
            if first:
                keys = split[1:]
                first = False
            else:
                self.teams[split[0]]["spteams_returning"] = dict(zip(keys, split[1:]))
                self.teams[split[0]]["spteams_returning_rank"] = counter
                counter += 1

    def print_team(self, team):
        print(
            '{}:\n\tTotal Offense {}:{}\n\tTotal Defense {}:{}\n\tPassing Offense {}:{}\n\tPassing Defense {}:{}\n\tRushing Offense {}:{}\n\tRushing Defense {}:{}\n\tPunting {}:{}\n\tReturning {}:{}'.format(
                team,
                self.teams[team]['total_offense_rank'], self.teams[team]['total_offense'],
                self.teams[team]['total_defense_rank'], self.teams[team]['total_defense'],
                self.teams[team]['passing_offense_rank'], self.teams[team]['passing_offense'],
                self.teams[team]['passing_defense_rank'], self.teams[team]['passing_defense'],
                self.teams[team]['rushing_offense_rank'], self.teams[team]['rushing_offense'],
                self.teams[team]['rushing_defense_rank'], self.teams[team]['rushing_defense'],
                self.teams[team]['spteams_punting_rank'], self.teams[team]['spteams_punting'],
                self.teams[team]['spteams_returning_rank'], self.teams[team]['spteams_returning'], ))

    def get_all_teams(self):
        keys = list(self.teams.keys())
        keys.sort()
        output = ''
        teamList = []
        for team in keys:
            output += team + '\n'
            teamList.append(team)
        return teamList

    def rank_by_sum(self):
        total_rank = {}
        for team in self.teams.keys():
            sum = self.teams[team]['total_offense_rank'] + self.teams[team]['total_defense_rank'] +self.teams[team]['passing_offense_rank'] \
            + self.teams[team]['passing_defense_rank'] + self.teams[team]['rushing_offense_rank'] + self.teams[team]['rushing_defense_rank'] \
            + self.teams[team]['spteams_punting_rank'] + self.teams[team]['spteams_returning_rank']
            total_rank[team] = sum
        sorted_rank = sorted(total_rank.items(), key=operator.itemgetter(1))
        count = 0
        output = ''
        while (count < 25):
            output += (str(sorted_rank[count]))
            count += 1
        return output

    def get_schedule_to_date(self, team):
        schedule = self.schedules[team]
        past_schedule = {}
        today = datetime.now()
        for game in schedule.keys():
            if datetime.strptime(schedule[game]['date'], '%m/%d/%Y') < today:
                past_schedule[game] = schedule[game]
        return past_schedule

    def get_opponent_stats_to_date(self, team):
        past_sch = self.get_schedule_to_date(team)
        to = 0
        td = 0
        po = 0
        pd = 0
        ro = 0
        rd = 0
        spp = 0
        spr = 0
        count = 0
        for opp in past_sch.keys():
            if opp in self.teams:
                to += int(self.teams[opp]['total_offense_rank'])
                td += int(self.teams[opp]['total_defense_rank'])
                po += int(self.teams[opp]['passing_offense_rank'])
                pd += int(self.teams[opp]['passing_defense_rank'])
                ro += int(self.teams[opp]['rushing_offense_rank'])
                rd += int(self.teams[opp]['rushing_defense_rank'])
                spp += int(self.teams[opp]['spteams_punting_rank'])
                spr += int(self.teams[opp]['spteams_returning_rank'])
            else:
                to += 80
                td += 80
                po += 80
                pd += 80
                ro += 80
                rd += 80
                spp += 80
                spr += 80
            count += 1
        to = to/count
        td = td / count
        po = po / count
        pd = pd / count
        ro = ro / count
        rd = rd / count
        spp = spp / count
        spr = spr / count
        return {'avg_total_offense_rank':to, 'avg_total_defense_rank':td, 'avg_passing_offense_rank':po, 'avg_passing_defense_rank':pd, 'avg_rushing_offense_rank':ro, 'avg_rushing_defense_rank':rd, 'avg_spteams_punting_rank':spp, 'avg_spteams_returning_rank':spr}

    def get_adj_ratings(self, team):
        ratings = {}
        teamStats = self.teams[team]
        teamOpp = self.get_opponent_stats_to_date(team)

        tot_off_pct = (128-teamStats['total_offense_rank'])/128
        avg_opp_tot_def_pct = (128-teamOpp['avg_total_defense_rank'])/128
        ratings['tot_off_rating'] = tot_off_pct * avg_opp_tot_def_pct

        tot_def_pct = (128 - teamStats['total_defense_rank']) / 128
        avg_opp_tot_off_pct = (128 - teamOpp['avg_total_offense_rank']) / 128
        ratings['tot_def_rating'] = tot_def_pct * avg_opp_tot_off_pct

        pass_off_pct = (128 - teamStats['passing_offense_rank']) / 128
        avg_opp_pass_def_pct = (128 - teamOpp['avg_passing_defense_rank']) / 128
        ratings['pass_off_rating'] = pass_off_pct * avg_opp_pass_def_pct

        pass_def_pct = (128 - teamStats['passing_defense_rank']) / 128
        avg_opp_pass_off_pct = (128 - teamOpp['avg_passing_offense_rank']) / 128
        ratings['pass_def_rating'] = pass_def_pct * avg_opp_pass_off_pct

        rush_off_pct = (128 - teamStats['rushing_offense_rank']) / 128
        avg_opp_rush_def_pct = (128 - teamOpp['avg_rushing_defense_rank']) / 128
        ratings['rush_off_rating'] = rush_off_pct * avg_opp_rush_def_pct

        rush_def_pct = (128 - teamStats['rushing_defense_rank']) / 128
        avg_opp_rush_off_pct = (128 - teamOpp['avg_rushing_offense_rank']) / 128
        ratings['rush_def_rating'] = rush_def_pct * avg_opp_rush_off_pct

        spp_pct = (128 - teamStats['spteams_punting_rank']) / 128
        avg_opp_spr_pct = (128 - teamOpp['avg_spteams_returning_rank']) / 128
        ratings['spp_rating'] = spp_pct * avg_opp_spr_pct

        spr_pct = (128 - teamStats['spteams_returning_rank']) / 128
        avg_opp_spp_pct = (128 - teamOpp['avg_spteams_punting_rank']) / 128
        ratings['spr_rating'] = spr_pct * avg_opp_spp_pct

        return ratings

    def get_comparison_report(self, teamA, teamB):
        teamAStats = self.teams[teamA]
        teamBStats = self.teams[teamB]
        teamAOpp = self.get_opponent_stats_to_date(teamA)
        teamBOpp = self.get_opponent_stats_to_date(teamB)
        teamARatings = self.get_adj_ratings(teamA)
        teamBRatings = self.get_adj_ratings(teamB)

        directComp = []
        directComp.append(('Total Offense', teamAStats['total_offense_rank'], '+' if teamAStats['total_offense_rank']<teamBStats['total_defense_rank'] else '-', teamBStats['total_offense_rank']))
        directComp.append(('Total Defense', teamAStats['total_defense_rank'], '+' if teamAStats['total_defense_rank']<teamBStats['total_offense_rank'] else '-', teamBStats['total_defense_rank']))
        directComp.append(('Passing Offense', teamAStats['passing_offense_rank'], '+' if teamAStats['passing_offense_rank']<teamBStats['passing_defense_rank'] else '-', teamBStats['passing_offense_rank']))
        directComp.append(('Passing Defense', teamAStats['passing_defense_rank'], '+' if teamAStats['passing_defense_rank']<teamBStats['passing_offense_rank'] else '-', teamBStats['passing_defense_rank']))
        directComp.append(('Rushing Offense', teamAStats['rushing_offense_rank'], '+' if teamAStats['rushing_offense_rank']<teamBStats['rushing_defense_rank'] else '-', teamBStats['rushing_offense_rank']))
        directComp.append(('Rushing Defense', teamAStats['rushing_defense_rank'], '+' if teamAStats['rushing_defense_rank']<teamBStats['rushing_offense_rank'] else '-', teamBStats['rushing_defense_rank']))
        directComp.append(('SpTeams Punting', teamAStats['spteams_punting_rank'], '+' if teamAStats['spteams_punting_rank']<teamBStats['spteams_returning_rank'] else '-', teamBStats['spteams_punting_rank']))
        directComp.append(('SpTeams Returning', teamAStats['spteams_returning_rank'], '+' if teamAStats['spteams_returning_rank']<teamBStats['spteams_punting_rank'] else '-', teamBStats['spteams_returning_rank']))

        oppAvgs = []
        oppAvgs.append(('Total Offense', '{:3.2f}'.format(teamAOpp['avg_total_offense_rank']), '{:3.2f}'.format(teamBOpp['avg_total_offense_rank'])))
        oppAvgs.append(('Total Defense', '{:3.2f}'.format(teamAOpp['avg_total_defense_rank']), '{:3.2f}'.format(teamBOpp['avg_total_defense_rank'])))
        oppAvgs.append(('Passing Offense', '{:3.2f}'.format(teamAOpp['avg_passing_offense_rank']), '{:3.2f}'.format(teamBOpp['avg_passing_offense_rank'])))
        oppAvgs.append(('Passing Defense', '{:3.2f}'.format(teamAOpp['avg_passing_defense_rank']), '{:3.2f}'.format(teamBOpp['avg_passing_defense_rank'])))
        oppAvgs.append(('Rushing Offense', '{:3.2f}'.format(teamAOpp['avg_rushing_offense_rank']), '{:3.2f}'.format(teamBOpp['avg_rushing_offense_rank'])))
        oppAvgs.append(('Rushing Defense', '{:3.2f}'.format(teamAOpp['avg_rushing_defense_rank']), '{:3.2f}'.format(teamBOpp['avg_rushing_defense_rank'])))
        oppAvgs.append(('SpTeams Punting', '{:3.2f}'.format(teamAOpp['avg_spteams_punting_rank']), '{:3.2f}'.format(teamBOpp['avg_spteams_punting_rank'])))
        oppAvgs.append(('SpTeams Returning', '{:3.2f}'.format(teamAOpp['avg_spteams_returning_rank']), '{:3.2f}'.format(teamBOpp['avg_spteams_returning_rank'])))

        adjRat = []
        adjRat.append(('Total Offense', '{:1.3f}'.format(teamARatings['tot_off_rating']), '+' if teamARatings['tot_off_rating']>teamBRatings['tot_def_rating'] else '-', '{:10.3f}'.format(teamBRatings['tot_off_rating'])))
        adjRat.append(('Total Defense', '{:1.3f}'.format(teamARatings['tot_def_rating']), '+' if teamARatings['tot_def_rating']>teamBRatings['tot_off_rating'] else '-', '{:10.3f}'.format(teamBRatings['tot_def_rating'])))
        adjRat.append(('Passing Offense', '{:1.3f}'.format(teamARatings['pass_off_rating']), '+' if teamARatings['pass_off_rating']>teamBRatings['pass_def_rating'] else '-', '{:10.3f}'.format(teamBRatings['pass_off_rating'])))
        adjRat.append(('Passing Defense', '{:1.3f}'.format(teamARatings['pass_def_rating']), '+' if teamARatings['pass_def_rating']>teamBRatings['pass_off_rating'] else '-', '{:10.3f}'.format(teamBRatings['pass_def_rating'])))
        adjRat.append(('Rushing Offense', '{:1.3f}'.format(teamARatings['rush_off_rating']), '+' if teamARatings['rush_off_rating']>teamBRatings['rush_def_rating'] else '-', '{:10.3f}'.format(teamBRatings['rush_off_rating'])))
        adjRat.append(('Rushing Defense', '{:1.3f}'.format(teamARatings['rush_def_rating']), '+' if teamARatings['rush_def_rating']>teamBRatings['rush_off_rating'] else '-', '{:10.3f}'.format(teamBRatings['rush_def_rating'])))
        adjRat.append(('SpTeams Punting', '{:1.3f}'.format(teamARatings['spp_rating']), '+' if teamARatings['spp_rating']>teamBRatings['spr_rating'] else '-', '{:10.3f}'.format(teamBRatings['spp_rating'])))
        adjRat.append(('SpTeams Returning', '{:1.3f}'.format(teamARatings['spr_rating']), '+' if teamARatings['spr_rating']>teamBRatings['spp_rating'] else '-', '{:10.3f}'.format(teamBRatings['spr_rating'])))



        output = ''
        output += ('\t\t\t{}\t\t{}\n'.format(teamA, teamB))
        output += ('-----------------------------------------\n')
        output += ('{:>10}{:^5}{:^5}{:^5}\n'.format('Total Off', teamAStats['total_offense_rank'], '+' if teamAStats['total_offense_rank']<teamBStats['total_defense_rank'] else '-', teamBStats['total_offense_rank']))
        output += ('{:>10}{:^5}{:^5}{:^5}\n'.format('Total Def', teamAStats['total_defense_rank'], '+' if teamAStats['total_defense_rank']<teamBStats['total_offense_rank'] else '-', teamBStats['total_defense_rank']))
        output += ('{:>10}{:^5}{:^5}{:^5}\n'.format('Pass Off', teamAStats['passing_offense_rank'], '+' if teamAStats['passing_offense_rank']<teamBStats['passing_defense_rank'] else '-', teamBStats['passing_offense_rank']))
        output += ('{:>10}{:^5}{:^5}{:^5}\n'.format('Pass Def', teamAStats['passing_defense_rank'], '+' if teamAStats['passing_defense_rank']<teamBStats['passing_offense_rank'] else '-', teamBStats['passing_defense_rank']))
        output += ('{:>10}{:^5}{:^5}{:^5}\n'.format('Rush Off', teamAStats['rushing_offense_rank'], '+' if teamAStats['rushing_offense_rank']<teamBStats['rushing_defense_rank'] else '-', teamBStats['rushing_offense_rank']))
        output += ('{:>10}{:^5}{:^5}{:^5}\n'.format('Rush Def', teamAStats['rushing_defense_rank'], '+' if teamAStats['rushing_defense_rank']<teamBStats['rushing_offense_rank'] else '-', teamBStats['rushing_defense_rank']))
        output += ('{:>10}{:^5}{:^5}{:^5}\n'.format('Sp Punt', teamAStats['spteams_punting_rank'], '+' if teamAStats['spteams_punting_rank']<teamBStats['spteams_returning_rank'] else '-', teamBStats['spteams_punting_rank']))
        output += ('{:>10}{:^5}{:^5}{:^5}\n'.format('Sp Ret', teamAStats['spteams_returning_rank'], '+' if teamAStats['spteams_returning_rank']<teamBStats['spteams_punting_rank'] else '-', teamBStats['spteams_returning_rank']))
        output += ('-----------------------------------------\n')
        output += ('Average Opponent Ranking\n')
        output += ('-----------------------------------------\n')
        output += ('Tot Off\t\t{}\t\t\t{}\n'.format(teamAOpp['avg_total_offense_rank'], teamBOpp['avg_total_offense_rank']))
        output += ('Tot Def\t\t{}\t\t\t{}\n'.format(teamAOpp['avg_total_defense_rank'], teamBOpp['avg_total_defense_rank']))
        output += ('Pass Off\t{}\t\t\t{}\n'.format(teamAOpp['avg_passing_offense_rank'], teamBOpp['avg_passing_offense_rank']))
        output += ('Pass Def\t{}\t\t\t{}\n'.format(teamAOpp['avg_passing_defense_rank'], teamBOpp['avg_passing_defense_rank']))
        output += ('Rush Off\t{}\t\t\t{}\n'.format(teamAOpp['avg_rushing_offense_rank'], teamBOpp['avg_rushing_offense_rank']))
        output += ('Rush Def\t{}\t\t\t{}\n'.format(teamAOpp['avg_rushing_defense_rank'], teamBOpp['avg_rushing_defense_rank']))
        output += ('Sp Punt\t\t{}\t\t\t{}\n'.format(teamAOpp['avg_spteams_punting_rank'], teamBOpp['avg_spteams_punting_rank']))
        output += ('Sp Ret\t\t{}\t\t\t{}\n\n'.format(teamAOpp['avg_spteams_returning_rank'], teamBOpp['avg_spteams_returning_rank']))
        output += ('-----------------------------------------\n')
        output += ('Adjusted Ratings Based On Opponents\n')
        output += ('-----------------------------------------\n')
        output += ('Tot Off\t\t{:10.3f}\t\t{}\t\t{:10.3f}\n'.format(teamARatings['tot_off_rating'], '+' if teamARatings['tot_off_rating']>teamBRatings['tot_def_rating'] else '-', teamBRatings['tot_off_rating']))
        output += ('Tot Def\t\t{:10.3f}\t\t{}\t\t{:10.3f}\n'.format(teamARatings['tot_def_rating'], '+' if teamARatings['tot_def_rating']>teamBRatings['tot_off_rating'] else '-', teamBRatings['tot_def_rating']))
        output += ('Pass Off\t{:10.3f}\t\t{}\t\t{:10.3f}\n'.format(teamARatings['pass_off_rating'], '+' if teamARatings['pass_off_rating']>teamBRatings['pass_def_rating'] else '-', teamBRatings['pass_off_rating']))
        output += ('Pass Def\t{:10.3f}\t\t{}\t\t{:10.3f}\n'.format(teamARatings['pass_def_rating'], '+' if teamARatings['pass_def_rating']>teamBRatings['pass_off_rating'] else '-', teamBRatings['pass_def_rating']))
        output += ('Rush Off\t{:10.3f}\t\t{}\t\t{:10.3f}\n'.format(teamARatings['rush_off_rating'], '+' if teamARatings['rush_off_rating']>teamBRatings['rush_def_rating'] else '-', teamBRatings['rush_off_rating']))
        output += ('Rush Def\t{:10.3f}\t\t{}\t\t{:10.3f}\n'.format(teamARatings['rush_def_rating'], '+' if teamARatings['rush_def_rating']>teamBRatings['rush_off_rating'] else '-', teamBRatings['rush_def_rating']))
        output += ('Sp Punt\t\t{:10.3f}\t\t{}\t\t{:10.3f}\n'.format(teamARatings['spp_rating'], '+' if teamARatings['spp_rating']>teamBRatings['spr_rating'] else '-', teamBRatings['spp_rating']))
        output += ('Sp Ret\t\t{:10.3f}\t\t{}\t\t{:10.3f}\n'.format(teamARatings['spr_rating'], '+' if teamARatings['spr_rating']>teamBRatings['spp_rating'] else '-', teamBRatings['spr_rating']))

        return directComp, oppAvgs, adjRat