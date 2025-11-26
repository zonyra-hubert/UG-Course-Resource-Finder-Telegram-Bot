import os

from dotenv import load_dotenv # NEW LINE 1

load_dotenv()

import telebot

from django import setup # Used to access Django models

# Initialize Django environment to access models
# This must be done before importing models
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ug_resource_bot.settings")
setup()

from course_data.models import Course

# Load BOT_TOKEN from .env
load_dotenv()
BOT_TOKEN = os.environ.get('BOT_TOKEN')

bot = telebot.TeleBot(BOT_TOKEN)

# Handler for /start command
@bot.message_handler(commands=['start'])
def send_welcome(message):
    welcome_text = (
        "👋 Welcome to the UG Course Finder Bot! \n"
        "I can help you find course details, credit hours, and resource links.\n\n"
        "**To find a course:** Type /find followed by the course code (e.g., /find DCIT203).\n\n"
        "To find the courses you will be doing in a specific level and semester, type /level followed by the level and semester (e.g., /level 200 sem1).\n"
        
    )
    bot.reply_to(message, welcome_text, parse_mode='Markdown')

#Handler for /level command
@bot.message_handler(commands=['level'])
def find_courses_by_level(message):
    try:
        parts = message.text.split()
        if len(parts) < 3:
            bot.reply_to(message, "Please provide level and semester. Example: /level 200 sem1")
            return
            
        level = parts[1]
        semester = parts[2].lower()
        
        # Query the Django database for courses matching level and semester
        courses = Course.objects.filter(level=level, semester=semester)
        
        if not courses.exists():
            bot.reply_to(message, f"❌ No courses found for level '{level}' and semester '{semester}'.")
            return
        
        response = f"📚 **Courses for Level {level} - {semester.capitalize()}:**\n\n"
        for course in courses:
            response += (
                f"**{course.code}: {course.title}**\n"
                f"Credits: {course.credits}\n"
                # f"Description: {course.description}\n"
            )
            if course.resource_link:
                response += f"🔗 **Resource Link:** [Click Here]({course.resource_link})\n"
            response += "\n"
        
        bot.reply_to(message, response, parse_mode='Markdown', disable_web_page_preview=True)
        
    except Exception as e:
        bot.reply_to(message, "An unexpected error occurred. Please try again later.")

# Handler for /find command
@bot.message_handler(commands=['find'])
def find_course(message):
    try:
        # 1. Extract the course code from the message text
        # Example: message.text is "/find DCIT203"
        parts = message.text.split()
        if len(parts) < 2:
            bot.reply_to(message, "Please provide a course code. Example: /find DCIT203")
            return
            
        course_code = parts[1].upper()
        
        # 2. Query the Django database
        course = Course.objects.get(code=course_code)
        
        # 3. Format the response
        response = (
            f"📚 **{course.code}: {course.title}**\n\n"
            f"Credits: {course.credits}\n"
            f"Description: {course.description}\n"
            
        )
        if course.resource_link:
             response += f"\n🔗 **Resource Link:** [Click Here]({course.resource_link})"
        
        bot.reply_to(message, response, parse_mode='Markdown', disable_web_page_preview=True)
        
    except Course.DoesNotExist:
        bot.reply_to(message, f"❌ Sorry, course code '{course_code}' not found in the database.")
    except Exception as e:
        # Generic error handling
        bot.reply_to(message, "An unexpected error occurred. Please try again later.")

# Start the bot polling loop
if __name__ == '__main__':
    print("Bot is starting...")
    bot.polling(none_stop=True)