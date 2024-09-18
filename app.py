from flask import Flask, request, redirect
import requests
import re

app = Flask(__name__)

@app.route('/youtube')
def youtube_search():
    url_param = request.args.get('id')
    
    if not url_param:
        return "Channel ID is required", 400

    # Remove the .m3u8 if it's part of the ID
    if url_param.endswith('.m3u8'):
        url_param = url_param[:-5]  # Remove '.m3u8'

    # Construct the YouTube live URL
    youtube_link = f'https://www.youtube.com/channel/{url_param}/live'
    target_url = 'https://www.azrotv.com/extras/youtube/'  # Replace this with the target URL
    payload = {'url': youtube_link}
    
    try:
        response = requests.post(target_url, data=payload)
        
        if response.status_code == 200:
            content = response.content.decode('utf-8-sig')  # Decoding with 'utf-8-sig' to remove BOM
            print("Response Content:", content)  # Print content for debugging
            
            # Extract m3u8 links from the content
            m3u8_links = re.findall(r'https?://[^\s]+\.m3u8', content)
            
            if m3u8_links:
                # Redirect to the first m3u8 link found
                return redirect(m3u8_links[0])
            else:
                return "No .m3u8 links found in the response.", 404
        else:
            return f"Error: {response.status_code}", 500
    except Exception as e:
        return f"An error occurred: {str(e)}", 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
