import csv
import re
print("hello")
#the scorers have been anonymised
scorer_list=['A A', 'A B', 'A C', 'A D',
'A E', 'A F', 'A H', 'A J',
'A K', 'A L', 'A M','A G']
game_list=[]
scorer_stats=["scorer name","games scored", "games won", "win percentage", "balls faced", 
"balls bowled","total balls scored","runs gained","runs conceded","runs scored", "wickets taken",
"wickets lost","wickets scored","number of teams scored for","overs faced", 
"overs bowled","total overs scored"]
scorer_data=[]
with open('scorecard2.csv', newline='') as csvfile:
    scorecards=csv.reader(csvfile)
    for row in scorecards:
        game_list.append(row)

def ball_into_over(balls):
    overs=balls//6
    balls_left=balls%6
    return str(overs)+"."+str(balls_left)

def ball_calculator(over):
    if over=='':
        return 0
    elif '.' in over:
        balls_list=str(over).split('.')
        return 6*int(balls_list[0])+int(balls_list[1])
    else:
        return 6*int(over)

def zero_check(num):
    if num=='':
        return 0
    else:
        return int(num)

for scorer in scorer_list:
    scorer_record=[scorer,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
    team_list=[]
    for row in game_list:
        if scorer in row:
            scorer_record[1]+=1
            if row[2] not in team_list:
                team_list.append(row[2])
            if "West Bridgfordians CC" in row[6]:
                scorer_record[2]+=1
            if "West Bridgfordians CC" in row[0]:
                scorer_record[4]+=ball_calculator(str(row[11]))
                scorer_record[5]+=ball_calculator(str(row[14]))
                scorer_record[7]+=zero_check(row[9])
                scorer_record[8]+=zero_check(row[12])
                scorer_record[10]+=zero_check(row[13])
                scorer_record[11]+=zero_check(row[10])
            if "West Bridgfordians CC" in row[1]:
                scorer_record[4]+=ball_calculator(str(row[14]))
                scorer_record[5]+=ball_calculator(str(row[11]))
                scorer_record[7]+=zero_check(row[12])
                scorer_record[8]+=zero_check(row[9])
                scorer_record[10]+=zero_check(row[10])
                scorer_record[11]+=zero_check(row[13])
    win_rate=100*scorer_record[2]//scorer_record[1]
    win_string=str(win_rate)+"%" 
    scorer_record[3]=win_string
    scorer_record[6]=scorer_record[4]+scorer_record[5]
    scorer_record[9]=scorer_record[7]+scorer_record[8]
    scorer_record[12]=scorer_record[11]+scorer_record[10]
    scorer_record[13]=len(team_list)
    scorer_data.append(scorer_record)

print(scorer_stats)
sum_row=["total",0,0,"n/a",0,0,0,0,0,0,0,0,0,"n/a",0,0,0]
for row in scorer_data:
    for j in range(len(sum_row)):
        if type(sum_row[j])==int:
            sum_row[j]+=row[j]

print(sum_row)
scorer_data.append(sum_row)

for row in scorer_data:
    row[14]=ball_into_over(row[4])
    row[15]=ball_into_over(row[5])
    row[16]=ball_into_over(row[6])


with open('scorer_data.csv', 'w') as f:
    csv_writer = csv.writer(f)
    csv_writer.writerow(scorer_stats)
    csv_writer.writerows(scorer_data)