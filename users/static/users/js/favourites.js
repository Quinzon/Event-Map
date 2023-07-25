$(document).ready(function() {
    $('.subscribe_to_profile').click(function() {
        var button = $(this);
        var profileId = button.data('profile-id');

        var data = {
            csrfmiddlewaretoken: CSRF_TOKEN,
            user_id: user_id,
            profile_id: profileId
        };

        $.ajax({
            url: '/user/toggle_profile_subscription/',
            method: 'POST',
            data: data,
            success: function(response) {
                if (response.subscribed) {
                    button.text('Вы подписаны');
                } else {
                    button.text('Подписаться');
                }
            }
        });
    });
});

$(document).ready(function() {
    $('.subscribe_to_event').click(function() {
    var button = $(this);
    var event_id = button.data('event-id');
    var event_id_number = parseInt(event_id);
    var isNumber = !isNaN(event_id_number);
    var data = {
        csrfmiddlewaretoken: CSRF_TOKEN,
        user_id: user_id,
        event_inner_id: !isNumber ? event_id : '',
        event_api_id: isNumber ? event_id : '',
    };

        $.ajax({
            url: '/toggle_event_subscription/',
            method: 'POST',
            data: data,
            success: function(response) {
                if (response.subscribed) {
                    button.text('Вы подписаны');
                } else {
                    button.text('Подписаться');
                }
            }
        });
    });
});

$(document).ready(function() {
    window.onload = function() {
        var choiceEvents = document.querySelector(".main-choice_events");
        var choiceProfiles = document.querySelector(".main-choice_profiles");

        var blockEvents = document.querySelector(".main-events");
        var blockProfiles = document.querySelector(".main-favorite_profiles");

        choiceEvents.addEventListener("click", function() {
            blockEvents.style.display = "flex";
            blockProfiles.style.display = "none";
            choiceEvents.classList.add("main-choice-selected");
            choiceProfiles.classList.remove("main-choice-selected");
        });

        choiceProfiles.addEventListener("click", function() {
            blockProfiles.style.display = "flex";
            blockEvents.style.display = "none";
            choiceProfiles.classList.add("main-choice-selected");
            choiceEvents.classList.remove("main-choice-selected");
        });
    }
});