window.mydom = null
$(document).ready(function () {
    mydom = $(".main-dom")
    // $('li').click(function(){
    //     $('li').css('color','#212529');
    //     $(this).css('color','red');
    // });
    mydom.find(".search").val("")
    mainscreen.fetch_user_notes()
});

mainscreen = {
    load_note: function (e) {
        file_name = $(e).text()
        file_name = file_name + ".html"
        $.ajax({
            type: 'GET',
            url: 'loadnote',
            data: { "filename": file_name }

        }).done(function (data) {
            $(".rightpane-display-area").text("").append("<p></P>")
            $(".rightpane-display-area").text("").append(data)

        });

    },

    resetmodel: function () {
        $(".chaptername").val("")
        $(".notearea").html("<p></p>")
        $(".file_name").val("")
        $("#save-btn").prop("disabled", true)
        $(".clone_loader").hide()
        mainscreen.step_count = 0

    },

    step_count: 0,
    add_step: function () {
        mainscreen.step_count = mainscreen.step_count + 1
        $(".notearea").append('<div class="step-header"><div class="stepname step' + mainscreen.step_count + '" contenteditable onkeyup="mainscreen.grabstep()">Step: ' + mainscreen.step_count + '</div></div><div class="description"><div class="description_ip desc' + mainscreen.step_count + '" data-text="Description here..." contenteditable></div></div>')


    },

    timeout: null,

    searchuserfromremote: function () {
        // var mydom = $("#mydom")
        // mydom.find(".remote_repos_list").html("<p></p>");
        // mydom.find(".repo_loader").show()
        username = mydom.find(".search").val().trim()
        // if (username.trim() != "") {
            if (mainscreen.timeout != null)
                clearTimeout(mainscreen.timeout)
            mainscreen.timeout = setTimeout(() => {
                // mydom.find(".remote_repos_list").html("<p></p>");
                if (username.trim() != "") {
                    mydom.find(".displayuser").text("").append("<p style='color:green; font-size:18px'>searching...</p>");
                }
                $.ajax({
                    type: 'GET',
                    url: 'search_user',
                    data: { "username": username }
                }).done(function (data) {
                    if (data == "success") {
                        if (username.trim() != "") {
                            mydom.find(".displayuser").text("");
                            mydom.find(".displayuser").text("").append("<a class='btn btn-info btn-sm fetch-btn' onclick='mainscreen.fetch_user_notes()'>Get notes</a>").css({ "color": "green", "font-style": "bold", "font-size": "18px", "margin-left": "10px" });
                        }
                    } else {
                        mydom.find(".repo_loader").hide()
                        mydom.find(".displayuser").text("no user found !").css({ "color": "red", "font-size": "18px", "margin-left": "10px" });
                    }
                })

            }, 1000);
        // } else {
        //     mydom.find(".repo_loader").hide()
        //     mydom.find(".displayuser").text("");
        //     mydom.find(".fetch-btn").hide();
        //     mydom.find(".remote_repos_list").html("<p></p>");

        // }

    },

    fetch_user_notes: function () {
        $(".notes-list").html("<p></p>");
        let username = mydom.find(".search").val().trim()
        if(username.trim() == ""){
            username = $("#mainuser").text().trim()
            if (username.trim() == ""){
                username = ""
                // list_items = "<div style='color:#f05959; text-align: center;'><b>Please login!</b></div>"
                // $(".notes-list").html('<ul>' + list_items + '</ul>')
            }
        }
        if(username.trim() != ""){
        $(".repo_loader").show()
        $.ajax({
            type: 'GET',
            url: 'fetch_user_notes',
            data: { "username": username }
        }).done(function (data) {
            if (data["status"] == "success") {
                $(".repo_loader").hide()
                repos = data["repo_list"]
                var i = 0;
                list_items = ""
                final_list = ""
                if (repos.length == 0) {
                    list_items = "<div style='color:#f05959; text-align: center;'><b>" + username + " doesn’t have any notes yet !</b></div>"
                }
                else {
                    for (i = 0; i < repos.length; i++) {
                        list_items += '<li onclick="mainscreen.load_note(this)">' + repos[i] + '</li>'
                    }
                }
                $(".notes-list").html('<ul>' + list_items + '</ul>')
                $('li').click(function () {
                    $('li').css('color', '#212529');
                    $(this).css('color', 'red');
                });
            }
            else if (data["status"] == "service_unavailable") {
                $(".repo_loader").hide()
                list_items = "<div style='color:#f05959; text-align: center;'><b>Service temporarily unavailable, please try again later !</b></div>"
                $(".notes-list").html(list_items)
            }
            else if(data["status"] == "fail"){
                $(".repo_loader").hide()
                list_items = "<div style='color:#f05959; text-align: center;'><b>" + username + " doesn’t have any notes yet !</b></div>"
                $(".notes-list").html(list_items)
            }
        })
    }
    },

    save: function () {
        $(".clone_loader").show()
        $("#save-btn").prop("disabled", true)
        total_steps = $(".stepname").length
        chapter_name = $(".chaptername").val()
        filename = $(".file_name").val()
        note_body = ""
        final_body = ""
        note_header = '<div class="note-header">' + chapter_name + '</div>'
        for (i = 1; i <= total_steps; i++) {
            step = ".step" + i
            desc = ".desc" + i
            step_name = $(step).html()
            desc = $(desc).html()
            note_body = note_body + '<div class="step-header">' + step_name + '</div><div class="description">' + desc + '</div>'
        }
        final_body = note_header + note_body
        $.ajax({
            type: "GET",
            url: "save_file",
            data: { "filename": filename, "finalbody": final_body }
        }).done(function (data) {
            if (data == "success") {
                $(".clone_loader").hide()
                $("#saveclose").trigger("click")
                mainscreen.synching()
                mainscreen.fetch_user_notes()

            }
            else {
                $(".clone_loader").hide()
                $("#saveclose").trigger("click")
                mainscreen.alert("Error", "something went wrong, unable to save notes !", "error")

            }
        })
    },

    enablesavebtn: function () {
        if (mainscreen.step_count >= 1 && ($(".file_name").val()).trim() != "") {
            $("#save-btn").prop("disabled", false)
        }
        else {
            $("#save-btn").prop("disabled", true)

        }
    },

    alert: function (header, message, message_type) {
        swal.fire(
            header,
            message,
            message_type
        )
    },

    synching : function(){
        Swal.fire({
            title: 'Synching!',
            html: 'Wait a moment please',
            timer: 2000,
            timerProgressBar: false,
            onBeforeOpen: () => {
              Swal.showLoading()
              timerInterval = setInterval(() => {
                const content = Swal.getContent()
                if (content) {
                  const b = content.querySelector('b')
                  if (b) {
                    b.textContent = Swal.getTimerLeft()
                  }
                }
              }, 300)
            },
            onClose: () => {
              clearInterval(timerInterval)
            }
          }).then((result) => {
            if (result.dismiss === Swal.DismissReason.timer) {
            }
          })
    },

    openloginform: function(){
        $(".loginform").show()
    },

    closeloginform: function(){
        $(".loginform").hide()
    },
    login(){
        username = $("#username").val()
        password = $("#password").val()
        console.log($(".token").val())
        if(username.trim() == "" || password.trim() == ""){
            $("#username").css({"border-color":"#c4c4c4"})
            $("#password").css({"border-color":"#c4c4c4"})
            if(username.trim() == ""){
            $("#username").css({"border-color":"red"})
            }
            if(password.trim() == ""){
                $("#password").css({"border-color":"red"})
            }
        }
        else{
            $("#username").css({"border-color":"#c4c4c4"})
            $("#password").css({"border-color":"#c4c4c4"})
            $.ajax({
                headers: {
                    'X-CSRFToken': $(".token").val()
                },
                type: "POST",
                url: "login",
                data: { "username": username, "password": password }
            }).done(function (data) {
                if (data["status"] == "success") {
                    console.log("success", data["username"])
                    mainscreen.closeloginform()
                    $("#mainuser").text(username)
                    window.setTimeout(function(){window.location.reload()}, 1000)
                    
    
                }
                else {
                    console.log("fail")
                    
                }
        })
        }
    },
    logout: function(){
        $.ajax({
            headers: {
                'X-CSRFToken': $(".token").val()
            },
            type: "POST",
            url: "logout",
            data: {}
        }).done(function (data) {
            if (data == "success") {
                window.setTimeout(function(){window.location.reload()}, 1000)
                console.log("success")
            }
            else {
                console.log("fail")
                
            }
    })

    }
}