var feedContent = $("#feed-input").val();
var userName = $("#username").text();
var type = $("#type").text();

$("#send-feed-message").click(function () {
    feedContent = $("#feed-input").val();
    alert(feedContent+userName+type);
    const xhr = new XMLHttpRequest();
    xhr.open('POST', '/feed/send');
    xhr.setRequestHeader('Content-Type', 'application/json');
    xhr.onload = function () {
        if (xhr.status == 200) {
            console.log(xhr.responseTest);
        }
    };
    
    xhr.send(JSON.stringify({user: userName, type: type, content: feedContent}));
});

$(document).ready(function () {
    // let sorted_list = 
    xhr2.open("POSE", '/feed/get');
    xhr2.setRequestHeader('Content-Type', 'application/json');
    xhr2.onload = function() {
        if (xhr2.status == 200) {
            console.log(xhr2.responseTest);
        }
    }
})
