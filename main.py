import discord
from discord.ext import tasks
from selenium.webdriver.common.by import By
from selenium import webdriver
import json
import time
from config import TOKEN
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


intents = discord.Intents.all()
client = discord.Client(intents=intents)

@client.event   
async def on_ready():

    announceChannel = client.get_channel(1027317084813787196)

    @tasks.loop(seconds=90)
    async def scrape():
        with open("data.json","r") as data_file:
            data = json.load(data_file)
            data_file.close()
       
        options = webdriver.ChromeOptions()
        options.add_argument("start-maximized")
        driver = webdriver.Chrome()
        driver.get('https://www.espn.com/soccer/schedule')

        await announceChannel.send("Time for this week's games!")

        for i in range(7):

            WebDriverWait(driver,15).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/div/div/div/main/div[3]/div/div/section/div/section/div/div/div/div/div/div[26]/div/div[5]/div')))
            driver.find_element(By.XPATH, '/html/body/div[1]/div/div/div/main/div[3]/div/div/section/div/section/div/div/div/div/div/div[26]/div/div[5]/div').click()

            time.sleep(5)

            Tables = driver.find_elements(By.CLASS_NAME, "ResponsiveTable")

            for table in Tables:
                if table.find_elements(By.TAG_NAME, 'div')[0].text in data['leagues_available']:
                    teams = table.find_elements(By.TAG_NAME, 'span')
                    counter = 0
                    for team in teams:
                        if counter % 2 == 0:
                            home = team.find_elements(By.TAG_NAME, 'a')[1].text
                        else:
                            away = team.find_elements(By.TAG_NAME, 'a')[1].text
                            msg = await announceChannel.send(home + " vs. " + away)
                            await msg.add_reaction('⬆️')
                        counter += 1

        await announceChannel.send("That's all for this week!")

        driver.quit()


    scrape.start()

    print('We have logged in as {0.user}'.format(client))

client.run(TOKEN)