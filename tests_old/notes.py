user_agent_values = {

    'key':
        {
            'platform': 'Mobile',
            'browser': 'No',
            'device': 'Android'
        },

    'Mozilla/5.0 (Linux; U; Android 4.0.2; en-us; Galaxy Nexus Build/ICL53F) AppleWebKit/534.30 (KHTML, like Gecko) Version/4.0 Mobile Safari/534.30':
        {
            'platform': 'Mobile',
            'browser': 'No',
            'device': 'Android'
        },

    'Mozilla/5.0 (iPad; CPU OS 13_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) CriOS/91.0.4472.77 Mobile/15E148 Safari/604.1':
        {
            'platform': 'Mobile',
            'browser': 'Chrome',
            'device': 'iOS'
        },

    'Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)':
        {
            'platform': 'Googlebot',
            'browser': 'Unknown',
            'device': 'Unknown'
        }
}


print(user_agent_values.keys(), end='\n')
raise KeyError("")