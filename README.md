Web UI Interact
===============

An Eva plugin that allows users to interact with Eva through the Web UI.

Useful for testing out new plugins without needing to send audio through clients.

![Web UI Interact](/screenshot.png?raw=true "https://127.0.0.1:8080/interact")

## Installation

Can be easily installed through the Web UI by using [Web UI Plugins](https://github.com/edouardpoitras/eva-web-ui-plugins).

Alternatively, add `web_ui_interact` to your `eva.conf` file in the `enabled_plugins` option list and restart Eva.

## Usage

Enable the plugin, go the the Web UI, and click on the new menu item titled `Interact`.

If you wish to send audio query/commands to Eva, you will need to allow the page to gain access to your microphone when prompted.

#### Send Text

You can send text directly to Eva for processing. Either type in the text manually, or use your browser's speech recognition implementation (limited support) to transcribe your voice into the text that Eva will process.

Note: This does not utilize a voice recognition Eva plugin as Eva never receives the audio.

#### Send Audio

You can send audio directly to Eva by following these steps:

1. Click on the `Record Audio` button (the button should now say `Stop Recording`)
2. Speak your query/command
3. Click on the `Stop Recording` button
4. Listen to the audio data you will send Eva by clicking on the `Play Audio` button (Optional)
5. Click on the `Send Audio` button to send the audio data to Eva for processing

Note: You need at least one voice recognition plugin enabled so that Eva can transribe audio to text for processing.

#### Eva Response

This is where Eva's response will appear after sending it a text or audio query/command.

You can check the `Play Audio Response` checkbox if you wish to listen to the response.

Note: You need a text-to-speech plugin enabled for Eva to respond with audio.

## Configuration

None
