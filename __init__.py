# Python 3.6
import pandas as pd
import web as wb


urls = ('/*', 'test', '/test', 'index')

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
        border-left: 6px solid #1ba38e;

    }
    ul {
    }
    li {
        cursor: pointer;
    }
    .modal {
        display: none;
        position: fixed;
        z-index: 1;
        left: 0;
        top: 0;
        width: 100%;
        height: 100%;
        padding-top: 100px;
        background-color: rgba(0,0,0,0.4);
        margin: 0;
        border: 0;
        border-radius: 0px;
    }
    .modal_content {
        width: 80%;
        margin: auto;
        border: 0;
    }
    .close {
        float: right;
    }
    .close:hover {
        cursor: pointer;
    }
    input {
    border: 1px solid #eee;
    width: 99%;
    padding: 2px;
    margin: 2px;
    }
    textarea {
    width:99%;
    border: 1px solid #eee;
    min-height: 10em;
    resize: none;
    padding: 2px;
    margin: 2px;
    }
</style>
'''

scripts = '''
<script>
    function open_modal(modal_id) {
        document.getElementById(modal_id).style.display="block";
    }

    function close_modals() {
        var modals = document.getElementsByClassName('modal');
        for (var i = 0; i < modals.length; i++) {
            modals[i].style.display = "none";
        }
    }

    function show_element(element_id) {
        var selected_element = document.getElementById(element_id);
        if (selected_element.style.display == "block") {
            selected_element.style.display = "none";
        }
        else {
            selected_element.style.display = "block";
        }
    }
</script>
'''


class DataHolder:
    def __init__(self):
        self.lanes = pd.read_csv('data/lanes.csv', sep=';')
        self.works = pd.read_csv('data/works.csv', sep=';')
        self.tasks = pd.read_csv('data/tasks.csv', sep=';')

    def add_task(self, task):
        max_task_id = max([int(x[1:]) for x in self.tasks['TaskId']])
        next_task_id = 'T{}'.format(max_task_id + 1)
        self.tasks = self.tasks.append(pd.DataFrame([[next_task_id, task['task_header'], task['task_description'],
                                                      'W003', pd.to_datetime(task['task_date']), task['task_url']]],
                                                    columns=['TaskId', 'TaskName', 'TaskDescription',
                                                             'WorkId', 'TaskDueDate', 'TaskLink']))


class index:
    def GET(self):
        return 'Hello world'


class test:
    dh = DataHolder()

    def GET(self):
        ret = '''<!DOCTYPE html>
        <html xmlns="http://www.w3.org/1999/html" xmlns="http://www.w3.org/1999/html">
        <head>
        {0}
        {1}
        </head>
        <body>'''.format(styles, scripts)
        for l in range(len(self.dh.lanes)):
            lane_id = self.dh.lanes.iloc[l,:]['LaneId']
            ret += h4(self.dh.lanes.iloc[l,:]['LaneName'], onclick="show_element('{0}')".format(lane_id))
            div_content = ''
            for w in range(len(self.dh.works[self.dh.works['LaneId'] == lane_id])):
                div_content += '<p><b>{0}</b></p>'.format(self.dh.works[self.dh.works['LaneId'] == lane_id].iloc[w, :]['WorkName'])
                work_id = self.dh.works[self.dh.works['LaneId'] == lane_id].iloc[w, :]['WorkId']
                ul_content = []
                for t in range(len(self.dh.tasks[self.dh.tasks['WorkId'] == work_id])):
                    task = self.dh.tasks[self.dh.tasks['WorkId'] == work_id].iloc[t, :]
                    ul_content.append({'id': task['TaskId'],
                                       'text': task['TaskName'],
                                       'onclick': "open_modal('m_{0}')".format(task['TaskId'])})
                div_content += ul(ul_content, e_id=work_id)
            ret += div(div_content, e_id=lane_id,
                       style="border-left-color:{}".format(self.dh.lanes.loc[l, 'LaneColor']))
        for t in range(len(self.dh.tasks)):
            task = self.dh.tasks.iloc[t, :]
            div_content = ''
            div_content += "<span class='close' onclick='close_modals()'>X</span>"
            div_content += '<p><b>{0}</b></p>'.format(task['TaskName'])
            div_content += '<p><i>{0}</i></p>'.format(task['TaskDueDate'])
            div_content += '<textarea>{0}</textarea>'.format(task['TaskDescription'])
            div_content = div(div_content, class_name="modal_content")
            ret += div(div_content, e_id='m_{0}'.format(task['TaskId']), class_name='modal')
        ret += '<form method="POST">'
        div_content = ''
        div_content += "<span class='close' onclick='close_modals()'>X</span>"
        div_content += '<input type="text" name="task_header" value="Task header"/>'
        div_content += '<input type="date" name="task_date"/>'
        div_content += '<input type="url" name="task_url" value="http://"/><br>'
        div_content += '<textarea name="task_description"></textarea>'
        div_content += '<input type="submit"/>'
        div_content = div(div_content, class_name="modal_content")
        ret += div(div_content, e_id='task_input'.format(task['TaskId']), class_name='modal')
        ret += '</form>'
        ret += h4('Add task', onclick="open_modal('task_input')")
        # ret += '<input type="text" name="s_input" value="smth"></p></form>'
        ret += '</body>'
        return ret

    def POST(self):
        i = wb.web.input()
        print('smthing')
        print(i)
        self.dh.add_task(i)
        return self.GET()


def h4(content, onclick='', style=''):
    onclick = get_onclick(onclick)
    style = get_style(style)
    ret = '<h4{1}{2}>{0}</h4>'.format(content,
                                      onclick,
                                      style)
    return ret


def div(content, e_id='', class_name='', style=''):
    e_id = get_id(e_id)
    class_name = get_class(class_name)
    style = get_style(style)
    ret = '<div{1}{2}{3}>{0}</div>'.format(content,
                                           e_id,
                                           class_name,
                                           style)
    return ret


def ul(content, e_id='', class_name='', style=''):
    e_id = get_id(e_id)
    style = get_style(style)
    class_name = get_class(class_name)
    options = ''
    for c in content:
        c_onclick = get_onclick(c['onclick'])
        options += '<li{1}>{0}</li>'.format(c['text'],
                                            c_onclick)
    ret = '<ul{1}{2}{3}>{0}</ul>'.format(options,
                                         e_id,
                                         class_name,
                                         style)
    return ret


def get_class(class_name):
    ret = ' class="{0}"'.format(class_name) if len(class_name) > 0 else ''
    return ret


def get_style(style):
    ret = ' style="{0}"'.format(style) if len(style) > 0 else ''
    return ret


def get_id(e_id):
    ret = ' id="{0}"'.format(e_id) if len(e_id) > 0 else ''
    return ret


def get_onclick(onclick):
    ret = ' onclick="{0}"'.format(onclick) if len(onclick) > 0 else ''
    return ret


if __name__ == '__main__':
    app = wb.application(urls, globals())
    app.run()
