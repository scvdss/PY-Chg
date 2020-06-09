import os
import random
import time
import discord

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv('DISCORD_TOKEN')
client = discord.Client()

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('user-data-dir=selenium')
driver = webdriver.Chrome(chrome_options=chrome_options)

@client.event
async def on_ready():
	print(f'{client.user} has connected to the server!')

@client.event
async def on_member_join(member):
	await member.create_dm()
	await member.dm_channel.send(
		f'Hi {member.name}, I am the bot that will send you answers. Ignore and else!'
	)

@client.event
async def on_message(message):
	if message.author == client.user:
		return
	if message.content.startswith('!AMAK'):
		messagestring = message.content.split() #split message by spaces, 
		url = messagestring[1] #ignore first part of array as we dont need the command. Just the url
		filenamereturned = questionpull(url) #forward the url to the question pull and get the filename back
		# print(filenamereturned)
		await message.author.create_dm() #dm the boi who asked
		await message.author.dm_channel.send('Your Answer:', file=discord.File(f'/home/andrew/{filenamereturned}', filenamereturned)) #upload and send the file
		time.sleep(5)#wait 5 seconds then delete the temp file.
		os.remove(f'/home/andrew/{filenamereturned}')

def site_login(): #this function isnt used but can be added. Cookies are much better
	driver.get("https://www.chegg.com/auth?action=login") 
	assert "Sign In or Sign Up | Chegg.com" in driver.title  #check if i am in the right place
	time.sleep(2.5)
	username = driver.find_element_by_id("emailForSignIn")
	password = driver.find_element_by_id("passwordForSignIn")
	username.send_keys("") #Insert Chegg Email Here
	password.send_keys("") #Insert Chegg Password Here
	driver.find_element_by_name("login").click() #dis boi clicks on the submit button on the login page

def questionpull(url):
	driver.get(url)
	time.sleep(5)
	answer = driver.find_element_by_class_name('answer-given-body') #find the section of chegg website that starts with answer id
	sourceraw = answer.get_attribute('innerHTML') #get the code and store it as string
	sourceraw= sourceraw.replace("https://http://", "https://") #fix urls for websites
	sourcefixed = sourceraw.replace("//", "https://")  
	name =  random.randint(0,10) #create random name for question storage
	filename = "%s.html" % name #create html file out of string name
	with open(filename, "w") as f:  #createfilename
		f.write(sourcefixed) #write the file html code
	return filename 
client.run(TOKEN) #start bot and wait for sommand
