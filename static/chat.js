const socket = io.connect("http://localhost:5000");

var chatRoomType;
var userName = $(".user-name:first-child").text();
$("#user-profile").text(userName[0].toUpperCase());
var personalityType = $("#personality-type").text();

var mbti_chart = [
  [
    "",
    "ISTJ",
    "ISFJ",
    "INFJ",
    "INTJ",
    "ISTP",
    "ISFP",
    "INFP",
    "INTP",
    "ESTP",
    "ESFP",
    "ENFP",
    "ENTP",
    "ESTJ",
    "ESFJ",
    "ENFJ",
    "ENTJ",
  ],
  ["ISTJ", "", 50, 50, 75, 25, 25, 25, 25, 100, 50, 50, 50, 100, 75, 75, 100],
  ["ISFJ", 50, "", 75, 75, 25, 50, 50, 50, 100, 50, 50, 50, 75, 100, 100, 100],
  ["INFJ", 50, 75, "", 100, 25, 50, 75, 75, 100, 50, 50, 50, 75, 100, 100, 100],
  [
    "INTJ",
    75,
    75,
    100,
    "",
    25,
    50,
    75,
    100,
    100,
    50,
    50,
    50,
    75,
    100,
    100,
    100,
  ],
  ["ISTP", 25, 25, 25, 25, "", 100, 75, 75, 100, 100, 100, 100, 25, 50, 50, 50],
  ["ISFP", 25, 50, 50, 50, 100, "", 75, 75, 100, 100, 100, 100, 25, 50, 50, 50],
  ["INFP", 25, 50, 75, 75, 75, 75, "", 100, 100, 100, 100, 100, 25, 50, 75, 75],
  [
    "INTP",
    25,
    50,
    75,
    100,
    75,
    75,
    100,
    "",
    100,
    100,
    100,
    100,
    25,
    50,
    75,
    100,
  ],
  [
    "ESTP",
    100,
    100,
    100,
    100,
    100,
    100,
    100,
    100,
    "",
    50,
    50,
    50,
    100,
    100,
    100,
    100,
  ],
  ["ESFP", 50, 50, 50, 50, 100, 100, 100, 100, 50, "", 50, 50, 50, 50, 50, 50],
  ["ENFP", 50, 50, 50, 50, 100, 100, 100, 100, 50, 50, "", 50, 50, 75, 75, 75],
  ["ENTP", 50, 50, 50, 50, 100, 100, 100, 100, 50, 50, 50, "", 50, 75, 75, 100],
  [
    "ESTJ",
    100,
    100,
    100,
    100,
    25,
    25,
    25,
    25,
    100,
    50,
    50,
    50,
    100,
    "",
    50,
    50,
    50,
    100,
  ],
  ["ESFJ", 75, 100, 100, 100, 50, 50, 50, 50, 100, 50, 50, 75, 50, "", 75, 75],
  ["ENFJ", 75, 100, 100, 100, 50, 50, 75, 75, 100, 50, 75, 75, 50, 75, "", 100],
  [
    "ENTJ",
    100,
    100,
    100,
    100,
    50,
    50,
    75,
    100,
    100,
    50,
    75,
    100,
    50,
    75,
    100,
    "",
  ],
];

console.log(mbti_chart);
var weightList;
var typeLIst = mbti_chart[0].slice(1);
console.log(mbti_chart[0].slice(1));
for (let rowIdx = 1; rowIdx < mbti_chart.length; rowIdx++) {
  if (mbti_chart[rowIdx][0] == personalityType) {
    console.log(mbti_chart[rowIdx][0], mbti_chart[rowIdx].slice(1));
    weightList = mbti_chart[rowIdx].slice(1);
  }
}
var sortedTypes = sortWithWeights(typeLIst, weightList);

$("#chat-rooms-nav").html("");
$("#chat-rooms-nav").append(
  $('<div class="chat-rooms-nav-heading"><h3>Recommended</h3></div>')
);
for (types in sortedTypes) {
    if (types == 3) {
      $("#chat-rooms-nav").append(
        '<div class="chat-rooms-nav-heading"><h3>Non-recommended</h3></div>'
      );
    }
    $("#chat-rooms-nav").append(
      `<div class="type-room-nav-item" id="${sortedTypes[types]}-rnav">${sortedTypes[types]}</div>`
    );
}

function sortWithWeights(arr1, arr2) {
  const arrOfObjs = arr1.map((el, i) => ({ el, weight: arr2[i] }));
  arrOfObjs.sort((a, b) => b.weight - a.weight);
  return arrOfObjs.map((obj) => obj.el);
}

socket.on("message", (data) => {
  const { text, sender, time } = data;
  const messageElement = document.createElement("div");
  // messageElement.innerText = `[${time}] ${sender}: ${text}`;
  // document.getElementById('messages').appendChild(messageElement);
  let type = "server";

  if (!sender) {
    type = "server";
  } else if (sender == userName) {
    type = "self";
  } else {
    type = "other";
  }

  var outerDiv = $("<div>").addClass("chat-item chat-content-" + type);
  var innerDiv = $("<div>").addClass("chat-packet");

  var innerDivSN = $("<div>").addClass("sender-name");
  var innerDivMC = $("<div>").addClass("message-content");
  var innerDivTS = $("<div>").addClass("time-stamp");

  innerDivSN.text(sender);
  innerDivMC.text(text);
  innerDivTS.text(time);

  innerDiv.append(innerDivSN);
  innerDiv.append(innerDivMC);
  innerDiv.append(innerDivTS);

  outerDiv.append(innerDiv);

  $("#chat-body").append(outerDiv);

  $("#chat-body").scrollTop($("#chat-body")[0].scrollHeight);
});

// window.addEventListener("beforeunload", () => {
//   socket.emit("leave", { hallway: "my_hallway" });
// });

$(".type-room-nav-item").on("click", function () {
  const type = $(this).text();
  $(`#${chatRoomType}-rnav`).removeClass("entered-chat-room");
  chatRoomType = type;
  $(`#${chatRoomType}-rnav`).addClass("entered-chat-room");
  socket.emit("join", { hallway: type });
});

$("#send-text").on("click", function () {
  console.log("clicked text output function");
  let textToSend = $("#text-input").val();
  if (!textToSend) {
    return 0;
  } else {
    console.log(textToSend);
    socket.emit("message", JSON.stringify({ message: textToSend }));
    $("#text-input").val("");
  }
});

$("#leave-room").on("click", function () {
  console.log("left room");
  socket.emit("leave", {});
});
