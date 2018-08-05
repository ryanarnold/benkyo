
var currentIndex = 0;

function updateQuestion() {
    $('#question').html(reviewItems[currentIndex].question);
}

function finishReview() {
    var currentPath = window.location.pathname;

    $.ajax({
        url: currentPath + 'assessment/',
        dataType: 'json',
        data: {
            reviewItems: JSON.stringify(reviewItems)
        },
        success: function(result) {
            window.location.href = currentPath + 'end/';
        },
        error: function(xhr, status, error) {
          alert(error);
        }
    });
}

function checkAnswer() {
    var answer = $('#input-answer').val();
    var correctAnswer = reviewItems[currentIndex].answer;

    if (answer == correctAnswer) {
        reviewItems[currentIndex].correct = true;
        reviewItems[currentIndex].timeToAnswer = 1;
        alert('CORRECT!');
    } else {
        reviewItems[currentIndex].correct = false;
        reviewItems[currentIndex].timeToAnswer = 100;
        alert('WRONG!');
    }

    currentIndex += 1;

    if (currentIndex < reviewItems.length) {
        updateQuestion();
        $('#input-answer').val('');
    } else {
        finishReview();
    }
}

$('#btn-submit').mouseup(checkAnswer);
$('#input-answer').keyup(function (event) {
    if (event.which == 13) {
        checkAnswer();
    }
});
updateQuestion();