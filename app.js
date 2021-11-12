function add_element(container_id, content_template, content_data) {
    var template = document.getElementById(content_template).content;
    content_data.forEach(element => {
        var container = document.getElementById(element.lane).getElementsByClassName("task-container")[0];
        var clone = template.cloneNode(true);
        clone.querySelectorAll('span')[0].textContent = element.title
        clone.querySelectorAll('p')[0].textContent = element.description;
        container.appendChild(clone);
    });
}
var my_tasks = JSON.parse(data);

