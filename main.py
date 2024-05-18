import json
from PIL import Image, ImageDraw, ImageFont
from colors import *

taskComplete = open("mockdb/task_complete.json", "r")
taskCompleteData = json.load(taskComplete)
taskComplete.close()
tasks = open("mockdb/tasks.json", "r")
tasksData = json.load(tasks)
tasks.close()
teams = open("mockdb/team.json", "r")
teamsData = json.load(teams)
teams.close()
users = open("mockdb/user.json", "r")
usersData = json.load(users)
users.close()
categories = open("mockdb/category.json", "r")
categoriesData = json.load(categories)
categories.close()
team_users = open("mockdb/team_users.json", "r")
teamUsersData = json.load(team_users)
team_users.close()


def getWinningTeams():
    teamPoints = {}
    for team in teamsData:
        teamPoints[team["id"]] = 0
    for task in taskCompleteData:
        if task["correct"]:
            teamPoints[task["team_id"]] += 1
    winningTeams = []
    points = []
    for i in range(3):
        maxPoints = max(teamPoints.values())
        for team in teamsData:
            if teamPoints[team["id"]] == maxPoints:
                winningTeams.append(team["id"])
                points.append(maxPoints)
                teamPoints[team["id"]] = -1
                break
    return winningTeams, points

def getMostAnsweredTasks():
    taskCount = {}
    taskCorrect = {}
    for task in tasksData:
        taskCount[task["id"]] = 0
        taskCorrect[task["id"]] = 0
    for task in taskCompleteData:
        taskCount[task["task_id"]] += 1
        if task["correct"]:
            taskCorrect[task["task_id"]] += 1
    mostAnsweredTasks = []
    answers = []
    correctAnswers = []
    for i in range(3):
        maxAnswers = max(taskCount.values())
        for task in tasksData:
            if taskCount[task["id"]] == maxAnswers:
                mostAnsweredTasks.append(task["id"])
                answers.append(maxAnswers)
                correctAnswers.append(taskCorrect[task["id"]])
                taskCount[task["id"]] = -1
                break
    return mostAnsweredTasks, answers, correctAnswers


def getMostCorrectTasks():
    taskCount = {}
    taskCorrect = {}
    for task in tasksData:
        taskCount[task["id"]] = 0
        taskCorrect[task["id"]] = 0
    for task in taskCompleteData:
        taskCount[task["task_id"]] += 1
        if task["correct"]:
            taskCorrect[task["task_id"]] += 1
    mostCorrectTasks = []
    answers = []
    correctAnswers = []
    for i in range(3):
        maxCorrectAnswers = max(taskCorrect.values())
        for task in tasksData:
            if taskCorrect[task["id"]] == maxCorrectAnswers:
                mostCorrectTasks.append(task["id"])
                answers.append(taskCount[task["id"]])
                correctAnswers.append(maxCorrectAnswers)
                taskCorrect[task["id"]] = -1
                break
    return mostCorrectTasks, answers, correctAnswers


def getTeamMembers(teamId):
    # link table is team_users
    teamMembers = []
    for user in usersData:
        for teamUser in teamUsersData:
            if teamUser["team_id"] == teamId and teamUser["user_id"] == user["id"]:
                teamMembers.append(user["name"])
    return teamMembers


iglogo = Image.open("images/logo_full.png")
iglogo = iglogo.resize((int(iglogo.width * 0.9), int(iglogo.height * 0.9)))
vlogo = Image.open("images/verglas_v.png")
vlogo = vlogo.resize((int(vlogo.width * 0.15), int(vlogo.height * 0.15)))
print(vlogo.width)
im = Image.open("images/triangles.png")
iglogox = int((im.width - iglogo.width) / 2)
im.paste(iglogo, (iglogox, 36), iglogo)
im.paste(vlogo, (im.width - vlogo.width - 48, 36), vlogo)
draw = ImageDraw.Draw(im)
_, _, w, h = draw.textbbox((0, 0), "By Verglas", font=ImageFont.truetype('fonts/OpenSans-Bold.ttf', 36))
draw.text((im.width - w - 36, h + vlogo.height), "By Verglas", white, font=ImageFont.truetype('fonts/OpenSans-Bold.ttf', 36))
ImageDraw.Draw(im).rounded_rectangle([((im.width - 400) / 2, 300), ((im.width - 400) / 2+400, 300+650)], 20, fill=purple)
ImageDraw.Draw(im).rounded_rectangle([(iglogox - 400 / 2, 300), (iglogox - 400 / 2+400, 300+650)], 20, fill=purple)
ImageDraw.Draw(im).rounded_rectangle([((iglogox + iglogo.width) - 400 / 2, 300), ((iglogox + iglogo.width) - 400 / 2+400, 300+650)], 20, fill=purple)
draw = ImageDraw.Draw(im)
_, _, w, h = draw.textbbox((0, 0), "Winning Teams", font=ImageFont.truetype('fonts/OpenSans-SemiBold.ttf', 36))
draw.text(((im.width - w) / 2, 318), "Winning Teams", white, font=ImageFont.truetype('fonts/OpenSans-SemiBold.ttf', 36))
winningTeams = getWinningTeams()
for i in range(3):
    for team in teamsData:
        if team["id"] == winningTeams[0][i]:
            teamMembers = getTeamMembers(team["id"])
            teamName = team["name"]
            teamPoints = winningTeams[1][i]
    _, _, w, h = draw.textbbox((0, 0), f"{teamName} with {teamPoints} points", font=ImageFont.truetype('fonts/OpenSans-Light.ttf', 32))
    draw.text(((im.width - w) / 2, 318 + 36 + 32 + 64 + i * 128), f"{teamName} with {teamPoints} points", white, font=ImageFont.truetype('fonts/OpenSans-Light.ttf', 32))
    _, _, w, h = draw.textbbox((0, 0), f"Members: {', '.join(teamMembers)}", font=ImageFont.truetype('fonts/OpenSans-Light.ttf', 32))
    draw.text(((im.width - w) / 2, 318 + 36 + 32 + 64 + i * 128 + 32), f"Members: {', '.join(teamMembers)}", white, font=ImageFont.truetype('fonts/OpenSans-Light.ttf', 32))
draw = ImageDraw.Draw(im)
_, _, w, h = draw.textbbox((0, 0), "Most Answered Tasks", font=ImageFont.truetype('fonts/OpenSans-SemiBold.ttf', 36))
draw.text((iglogox - w / 2, 318), "Most Answered Tasks", white, font=ImageFont.truetype('fonts/OpenSans-SemiBold.ttf', 36))
mostAnsweredTasks = getMostAnsweredTasks()
for i in range(3):
    for task in tasksData:
        if task["id"] == mostAnsweredTasks[0][i]:
            for category in categoriesData:
                if category["id"] == task["category_id"]:
                    categoryName = category["name"]
            taskName = task["name"]
            taskAnswers = mostAnsweredTasks[1][i]
            taskCorrectAnswers = mostAnsweredTasks[2][i]
            taskContent = task["content"]
    _, _, w, h = draw.textbbox((0, 0), f"{taskName} with {taskAnswers} answers and {taskCorrectAnswers} correct answers in {categoryName}", font=ImageFont.truetype('fonts/OpenSans-Light.ttf', 32))
    draw.text((iglogox - w / 2, 318 + 36 + 32 + 64 + i * 128), f"{taskName} with {taskAnswers} answers and {taskCorrectAnswers} correct answers in {categoryName}", white, font=ImageFont.truetype('fonts/OpenSans-Light.ttf', 32))
draw = ImageDraw.Draw(im)
_, _, w, h = draw.textbbox((0, 0), "Most Correct Tasks", font=ImageFont.truetype('fonts/OpenSans-SemiBold.ttf', 36))
draw.text(((iglogox + iglogo.width) - w / 2, 318), "Most Correct Tasks", white, font=ImageFont.truetype('fonts/OpenSans-SemiBold.ttf', 36))
mostAnsweredTasks = getMostAnsweredTasks()
for i in range(3):
    for task in tasksData:
        if task["id"] == mostAnsweredTasks[0][i]:
            for category in categoriesData:
                if category["id"] == task["category_id"]:
                    categoryName = category["name"]
            taskName = task["name"]
            taskAnswers = mostAnsweredTasks[1][i]
            taskCorrectAnswers = mostAnsweredTasks[2][i]
            taskContent = task["content"]
    _, _, w, h = draw.textbbox((0, 0), f"{taskName} with {taskAnswers} answers and {taskCorrectAnswers} correct answers in {categoryName}", font=ImageFont.truetype('fonts/OpenSans-Light.ttf', 32))
    draw.text(((iglogox + iglogo.width) - w / 2, 318 + 36 + 32 + 64 + i * 128), f"{taskName} with {taskAnswers} answers and {taskCorrectAnswers} correct answers in {categoryName}", white, font=ImageFont.truetype('fonts/OpenSans-Light.ttf', 32))
im.show()