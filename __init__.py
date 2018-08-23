# Python 3.6
import pandas as pd
import web as wb

print('start')
lanes = pd.read_csv('data/lanes.csv', sep=';')
works = pd.read_csv('data/works.csv', sep=';')
tasks = pd.read_csv('data/tasks.csv', sep=';')

urls = ('/', 'test', '/test', 'test')

styles = '''
<style>
    body {
        background-color: #e8e8e8;
    }
    div {
        background-color: #fff;
        border-radius: 4px;
        padding: 1px;
        padding-left: 10px;
        padding-right: 10px;
        margin: 5px;

    }
</style>
'''


class index:
    def GET(self):
        return 'Hello world'

class test:
    def GET(self):
        ret = '''<!DOCTYPE html>
        <html xmlns="http://www.w3.org/1999/html" xmlns="http://www.w3.org/1999/html">
        <head>
        {0}
        </head>
        <body>'''.format(styles)
        for l in range(len(lanes)):
            lane_id = lanes.iloc[l,:]['LaneId']
            ret += '<div id={0}>{1}'.format(lane_id, lanes.iloc[l,:]['LaneName'])
            for w in range(len(works[works['LaneId'] == lane_id])):
                ret += '<p><b>{0}</b></p>'.format(works[works['LaneId'] == lane_id].iloc[w, :]['WorkName'])
                work_id = works[works['LaneId'] == lane_id].iloc[w, :]['WorkId']
                ret += '<ul>'
                for t in range(len(tasks[tasks['WorkId'] == work_id])):
                    _task = tasks[tasks['WorkId'] == work_id].iloc[t, :]
                    ret += '<li>{0} - {1}</li>'.format(_task['TaskId'], _task['TaskName'])
                ret += '</ul>'
            ret += '</div>'
        ret+='</body>'
        return ret


if __name__ == '__main__':
    app = wb.application(urls, globals())
    app.run()