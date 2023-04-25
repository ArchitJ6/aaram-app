var homeBtn = document.getElementById("home-href");
    var chatBtn = document.getElementById("chat-href");
    //var profileBtn = document.getElementById("profile-href");
    var reelsBtn = document.getElementById("reels-href");
    var consBtn = document.getElementById("consultancy-href");
    var logo=document.querySelector(".logo");
    var right_nav=document.querySelector(".right-nav");

    homeBtn.addEventListener("click", function (event) {
      window.location.href = "/dashboard";
      event.preventDefault();
    });
    chatBtn.addEventListener("click", function (event) {
      window.location.href = "/chat";
      event.preventDefault();
    });
    //profileBtn.addEventListener("click", function (event) {
    //  window.location.href = "";
    //  event.preventDefault();
    //});
    reelsBtn.addEventListener("click", function (event) {
      window.location.href = "/reels";
      event.preventDefault();
    });
    consBtn.addEventListener("click", function (event) {
      window.location.href = "";
      event.preventDefault();
    });
    right_nav.addEventListener("click", function (event) {
        window.location.href = "/profile";
        event.preventDefault();
      });
      logo.addEventListener("click", function (event) {
        window.location.href = "/dashboard";
        event.preventDefault();});