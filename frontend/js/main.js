$.ajaxSetup({
    beforeSend: function beforeSend(xhr, settings) {
        function getCookie(name) {
            let cookieValue = null;


            if (document.cookie && document.cookie !== '') {
                const cookies = document.cookie.split(';');

                for (let i = 0; i < cookies.length; i += 1) {
                    const cookie = jQuery.trim(cookies[i]);

                    // Does this cookie string begin with the name we want?
                    if (cookie.substring(0, name.length + 1) === (`${name}=`)) {
                        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                        break;
                    }
                }
            }

            return cookieValue;
        }

        if (!(/^http:.*/.test(settings.url) || /^https:.*/.test(settings.url))) {
            // Only send the token to relative URLs i.e. locally.
            xhr.setRequestHeader('X-CSRFToken', getCookie('csrftoken'));
        }
    },
});



// Modal
$(document).ready(function () {
    $('.js-toggle-modal').click(function () {
        $('.js-modal').removeClass('hidden').addClass('flex');
    });

    $('.js-close-modal').click(function () {
        $('.js-modal').removeClass('flex').addClass('hidden');
    });

    // Close modal when clicking outside the box
    $('.js-modal').click(function (e) {
        if (e.target === this) {
            $(this).removeClass('flex').addClass('hidden');
        }
    });

    // Sidebar toggle for small screens
    $('#sidebarToggle').click(function () {
        $('#sidebar').toggleClass('-translate-x-full');
    });
});

//create post
$(document).ready(function () {
$(document).on("click", ".js-submit", function (e) {
    e.preventDefault();
    console.log("clicked")
    const text = $(".js-post-text").val().trim();
    const $btn = $(this);
    if (!text.length) {
        return false;
    }

    $(".js-post-text").val("");

    $btn.prop("disabled", true).text("Posting!");
    $.ajax({
        url: $(".js-post-text").data("post-url"),
        type: "POST",
        data: {
            text: text,
        },
        success: function (dataHtml) {
            $(".js-modal").removeClass("flex").addClass("hidden");
            $("#posts-container").prepend(dataHtml);
            $btn.prop("disabled", false).text("New Post");
            $(".js-post-text").val("");
        },
        error: function (error) {
            console.warn(error);
            $btn.prop("disabled", false).text("Error");
        },
    });
})
$(document).on("click", ".js-follow", function (e) {
        e.preventDefault();
        const $btn = $(this);
        const action = $btn.data("action");

        $.ajax({
            url: $btn.data("url"),
            type: "POST",
            data: {
                action: action,
                username: $btn.data("username"),
            },
            success: (data) => {
                // 1️⃣ Update button text & data-action
                $btn.find(".js-follow-text").text(data.wording);
                $btn.data("action", data.wording.toLowerCase() === "unfollow" ? "unfollow" : "follow");
                $btn.toggleClass("bg-blue-500 hover:bg-blue-600 bg-red-500 hover:bg-red-600");

                // 2️⃣ Update the follower count on the page
                $(".js-total-followers").text(data.total_followers);
            },
            error: (err) => {
                console.warn(err);
            },
        });
});
   
});

