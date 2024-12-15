<div style="text-align:center;">
    <h1>Flask Face Detection with Effects</h1>
    <p>This project uses Flask and OpenCV to create a real-time video stream with facial recognition and various effects.</p>
    <p>Apply overlays like glasses, heart emojis, and even a dog image to faces detected in the video stream.</p>
</div>

<h2>Project Screenshot</h2>
<div style="text-align:center;">
    <img src="https://github.com/Ardacanuysal/SnapShot/blob/main/Ekran%20Resmi%202024-12-15%2014.39.26.png" alt="Project Screenshot" width="500"/>
</div>

<h3>Features:</h3>
<ul>
    <li>Real-time video streaming with face detection</li>
    <li>Apply overlays such as glasses, heart emoji, and dog images</li>
    <li>Control video effects like temperature, black & white, and contrast</li>
    <li>Option to activate or deactivate "Dog Encoding" (displays a message when active)</li>
</ul>

<h3>Installation Steps:</h3>
<ol>
    <li>Clone the repository</li>
    <li>Navigate to the project folder</li>
    <li>Create and activate a virtual environment</li>
    <li>Install dependencies using <code>pip install -r requirements.txt</code></li>
    <li>Start the Flask application using <code>python app.py</code></li>
</ol>

<h3>API Endpoints:</h3>
<ul>
    <li><code>/</code>: Displays the main page with video feed</li>
    <li><code>/video_feed</code>: Streams the video with face detection and effects</li>
    <li><code>/select_image</code> (POST): Select the image effect to apply (glasses, heart, emoji, dog)</li>
    <li><code>/set_contrast</code> (POST): Sets the contrast level of the video stream</li>
    <li><code>/start_dog_encoding</code> (POST): Activates the dog encoding effect</li>
    <li><code>/stop_dog_encoding</code> (POST): Deactivates the dog encoding effect</li>
</ul>

<h3>Example API Calls:</h3>
<pre>
  Set Contrast Level:
  curl -X POST http://127.0.0.1:5000/set_contrast -d '{"contrast": 70}' -H "Content-Type: application/json"
</pre>
<pre>
  Start Dog Encoding:
  curl -X POST http://127.0.0.1:5000/start_dog_encoding
</pre>
<pre>
  Stop Dog Encoding:
  curl -X POST http://127.0.0.1:5000/stop_dog_encoding
</pre>

<h3>License:</h3>
<p>This project is licensed under the MIT License. See the <code>LICENSE</code> file for details.</p>
