# Jinghua Zhang, Scott Faludi
# CS231 Spr 2021
# PB server script
# This is the main server that handles incoming and outgoing http requests

import requests
import flask
import PbInfoParse
import PbReadSpreadsheet

app = flask.Flask(__name__)


@app.route('/signup', methods=['POST'])
def response():
    PbInfoParse.parsing_information(flask.request.json)
    list_of_pb = [PbInfoParse.parsing_information(flask.request.json)]
    pb_name = PbInfoParse.writing_information(list_of_pb)
    response_list = PbReadSpreadsheet.retrieve_client_data(pb_name)
    r = requests.post("https://hooks.slack.com/services/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",
                      data=flask.jsonify(response_list))
    return flask.Response(status=200)


if __name__ == "__main__":
  app.run()