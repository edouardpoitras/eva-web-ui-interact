import os
import gossip
from flask import Response, make_response, render_template_string, request, jsonify, send_file, abort
from eva import director
from eva import conf
from eva import log

dir_path = os.path.dirname(os.path.realpath(__file__))
interact_markup = open(dir_path + '/templates/interact.html').read()
TEMP_AUDIO_FILE = '/tmp/web_ui_interact_audio'
TEMP_AUDIO_CONTENT_TYPE = '/tmp/web_ui_interact_ct'

@gossip.register('eva.web_ui.start', provides=['web_ui_interact'])
def web_ui_start(app):
    app.add_url_rule('/interact', 'interact', interact)
    app.add_url_rule('/interact/text', 'interact_text', interact_text)
    app.add_url_rule('/interact/audio', 'interact_audio', interact_audio, methods=['POST'])
    app.add_url_rule('/interact/response-audio', 'interact_response_audio', interact_response_audio)
    app.add_url_rule('/interact/recorder.js', 'interact_recorderjs', interact_recorderjs)

@gossip.register('eva.web_ui.menu_items', provides=['web_ui_interact'])
def web_ui_menu_items():
    menu_item = {'path': '/interact', 'title': 'Interact'}
    conf['plugins']['web_ui']['config']['menu_items'].append(menu_item)

def interact():
    menu_items = conf['plugins']['web_ui']['module'].ready_menu_items()
    return render_template_string(interact_markup, menu_items=menu_items)

def interact_audio():
    file_storage = request.files['data']
    ret = {'input_audio': {'audio': file_storage.read(), 'content_type': file_storage.content_type}}
    results = director.interact(ret)
    handle_temp_audio_file(results)
    return jsonify(results)

def handle_temp_audio_file(results):
    if 'output_audio' in results and type(results['output_audio']) == dict:
        f = open(TEMP_AUDIO_FILE, 'wb')
        f.write(results['output_audio'].get('audio', ''))
        f.close()
        f = open(TEMP_AUDIO_CONTENT_TYPE, 'w')
        f.write(results['output_audio'].get('content_type', None))
        f.close()
        # Don't send all this data back to the client.
        results['output_audio'] = True

def interact_text():
    input_text = request.args.get('input_text')
    results = director.interact({'input_text': input_text})
    handle_temp_audio_file(results)
    return jsonify(results)

def interact_response_audio():
    if not os.path.isfile(TEMP_AUDIO_FILE): abort(404)
    content_type = open(TEMP_AUDIO_CONTENT_TYPE).read()
    response = make_response(send_file(TEMP_AUDIO_FILE,
                                       mimetype=content_type,
                                       as_attachment=True,
                                       attachment_filename='eva_response'))
    response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    response.headers['Pragma'] = 'no-cache'
    return response

def interact_recorderjs():
    recorderjs = open(dir_path + '/recorder.js').read()
    return Response(recorderjs, mimetype='application/javascript')
