
import telebot
import requests
import re
from bs4 import BeautifulSoup



bot = telebot.TeleBot("6010415181:AAFQhNACAvirmVZFRjLCw5CXBtees5NXfUo")
affiliate_id = "dailyupdat0c9-21"
proxy_url = "https://cors-anywhere.herokuapp.com/"





def convert_amazon_link_to_affiliate_id(link, affiliate_id):
    # Retrieve HTML from Amazon product page
    link = proxy_url + link
    page = requests.get(link)
    soup = BeautifulSoup(page.content, 'html.parser')

    # Extract ASIN from HTML using regular expressions
    asin_pattern = r'/dp/([A-Z0-9]{10})'
    asin_match = re.search(asin_pattern, link)
    if asin_match:
        asin = asin_match.group(1)
    else:
        asin_tag = soup.find('input', {'name': 'ASIN'})
        if asin_tag:
            asin = asin_tag.get('value')
        else:
            return None

    # Construct affiliate ID link
    affiliate_link = f'https://www.amazon.in/dp/{asin}/?tag={affiliate_id}'

    return affiliate_link


def replace_amazon_link_with_affiliate_url(message, affiliate_url):
    # Replace Amazon link with encoded and shortened URL in message
    updated_text = message.text.replace(message.text, affiliate_url)

    # Return updated message
    return updated_text


def check_link_type(link):
    if 'ekaro.in' in link:
        return True
    elif 't.me' in link:
        return True
    elif 'wa.me' in link:
        return True
    else:
        return False


@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "Hello! Please enter your Amazon link to encode it with your affiliate ID.")


@bot.message_handler(func=lambda message: True)
def encode_url(message):
    # Extract all Amazon links from the channel message
    original_message = message.text
    link_pattern = r'(https?://[^\s]+)'
    links = re.findall(link_pattern, original_message)

    if not links:
        bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
        return

    encoded_message = original_message
    for amazon_link in links:



        affiliate_link = convert_amazon_link_to_affiliate_id(amazon_link, affiliate_id)

        if affiliate_link:
            # Encode and shorten affiliate link
            encoded_url = "https://dailyupdateblogg.blogspot.com/p/track.html?trackurl=" + affiliate_link
            response = requests.get(f"http://tinyurl.com/api-create.php?url={encoded_url}")
            shortened_url = response.text

            # Replace the Amazon link in the original message with the affiliate link
            encoded_message = encoded_message.replace(amazon_link, shortened_url)
        elif check_link_type(amazon_link):
            return

        else:
            invalid_message = bot.reply_to(message, "Invalid link.")
            bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
            bot.delete_message(chat_id=message.chat.id, message_id=invalid_message.message_id)
            return


    # Reply to user with the encoded message
    bot.reply_to(message, encoded_message)
    bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)



@bot.channel_post_handler(func=lambda message: True)
def encode_url_channel(message):
    original_message = message.text
    link_pattern = r'(https?://[^\s]+)'
    links = re.findall(link_pattern, original_message)

    if not links:
        bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
        return

    encoded_message = original_message
    for amazon_link in links:

        # Convert Amazon link to affiliate lin
        affiliate_link = convert_amazon_link_to_affiliate_id(amazon_link, affiliate_id)

        if affiliate_link:
            # Encode and shorten affiliate link
            encoded_url = "https://dailyupdateblogg.blogspot.com/p/track.html?trackurl=" + affiliate_link
            response = requests.get(f"http://tinyurl.com/api-create.php?url={encoded_url}")
            shortened_url = response.text

            # Replace the Amazon link in the original message with the affiliate link
            encoded_message = encoded_message.replace(amazon_link, shortened_url)
        elif check_link_type(amazon_link):
            return

        else:
            invalid_message = bot.reply_to(message, "Invalid link.")
            bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
            bot.delete_message(chat_id=message.chat.id, message_id=invalid_message.message_id)
            return


    # Reply to user with the encoded message
    bot.reply_to(message, encoded_message)
    bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)



bot.polling()
