
        // jQuery time
        var current_fs, next_fs, previous_fs; //fieldsets
        var left, opacity, scale; //fieldset properties which we will animate
        var animating; //flag to prevent quick multi-click glitches

        $(".next").click(function () {
            if (animating) return false;
            animating = true;

            current_fs = $(this).parent();
            next_fs = $(this).parent().next();

            // Check if all required fields in the current fieldset are filled
            var allFieldsFilled = true;
            current_fs.find('input[required], textarea[required], select[required]').each(function () {
                if ($(this).val() === '') {
                    allFieldsFilled = false;
                    return false; // Exit the loop early if a required field is empty
                }
            });

            if (!allFieldsFilled) {
                // Display an alert if not all required fields are filled
                alert("Please answer all questions before proceeding.");
                animating = false; // Reset the animating flag
                return false; // Prevent moving to the next fieldset
            }

            // Activate next step on progressbar using the index of next_fs
            $("#progressbar li").eq($("fieldset").index(next_fs)).addClass("active");

            // Show the next fieldset
            next_fs.show();
            // Hide the current fieldset with style
            current_fs.animate({ opacity: 0 }, {
                step: function (now, mx) {
                    // Animation code
                    scale = 1 - (1 - now) * 0.2;
                    left = (now * 50) + "%";
                    opacity = 1 - now;
                    current_fs.css({ 'transform': 'scale(' + scale + ')' });
                    next_fs.css({ 'left': left, 'opacity': opacity });
                },
                duration: 500,
                complete: function () {
                    current_fs.hide();
                    animating = false;
                },
                easing: 'easeOutQuint'
            });
        });

        $(".previous").click(function () {
            if (animating) return false;
            animating = true;

            current_fs = $(this).parent();
            previous_fs = $(this).parent().prev();

            // De-activate current step on progressbar
            $("#progressbar li").eq($("fieldset").index(current_fs)).removeClass("active");

            // Show the previous fieldset
            previous_fs.show();
            // Hide the current fieldset with style
            current_fs.animate({ opacity: 0 }, {
                step: function (now, mx) {
                    // Animation code
                    scale = 0.8 + (1 - now) * 0.2;
                    left = ((1 - now) * 50) + "%";
                    opacity = 1 - now;
                    current_fs.css({ 'left': left });
                    previous_fs.css({ 'transform': 'scale(' + scale + ')', 'opacity': opacity });
                },
                duration: 500,
                complete: function () {
                    current_fs.hide();
                    animating = false;
                },
                easing: 'easeOutQuint'
            });
        });

        $(".submit").click(function () {
            return false;
        });

        // Handle form submission
        $("#msform").submit(function (e) {
            e.preventDefault();
            // You can add code to handle form submission here
            $(".success-message").show(); // Display a success message
        });





$(document).ready(function() {
    // اختصارات لاختيار العناصر
    const videoFile = $('#video-file');
    const videoButton = $('#video-button');
    const videoIcon = $('#video-icon');

    // دالة لتشغيل أو إيقاف تشغيل الفيديو
    function playPause() {
        if (videoFile[0].paused) {
            // تشغيل الفيديو
            videoFile[0].play();
            // تغيير الرمز
            videoIcon.addClass('ri-pause-line').removeClass('ri-play-line');
        } else {
            // إيقاف تشغيل الفيديو
            videoFile[0].pause();
            // تغيير الرمز
            videoIcon.removeClass('ri-pause-line').addClass('ri-play-line');
        }
    }

    // استماع للنقر على زر التشغيل/الإيقاف
    videoButton.on('click', playPause);

    // دالة لتغيير الرمز عند انتهاء الفيديو
    function finalVideo() {
        // تغيير الرمز عند انتهاء الفيديو
        videoIcon.removeClass('ri-pause-line').addClass('ri-play-line');
    }

    // استماع لحدوث الحدث 'ended' عند انتهاء الفيديو
    videoFile.on('ended', finalVideo);
});
