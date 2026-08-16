// assets/js/chat.js
//
// Scripted assistant for the floating chat widget.
//
// Deliberately not AI-backed: the site is static, so an LLM call would mean
// either shipping an API key in the page or standing up a backend. This
// matches user questions against a keyword-scored topic list and hands off to
// WhatsApp whenever it cannot answer, which is where a real sales
// conversation should end up anyway.
//
// All copy lives in a JSON island (#chat-data) written by the generators, so
// this file is identical for English and Arabic.

(function () {
    'use strict';

    var dataEl = document.getElementById('chat-data');
    var panel = document.getElementById('chat-panel');
    if (!dataEl || !panel) return;

    var DATA;
    try {
        DATA = JSON.parse(dataEl.textContent);
    } catch (e) {
        console.error('chat-data is not valid JSON:', e);
        return;
    }

    var log = panel.querySelector('.chat-log');
    var replies = panel.querySelector('.chat-replies');
    var form = panel.querySelector('.chat-form');
    var input = form.querySelector('input');
    var toggle = document.getElementById('chat-toggle');
    var closeBtn = panel.querySelector('.chat-close');
    var started = false;

    // The scroll container is .chat-body (log + quick replies together), so
    // new messages and the reply buttons stay reachable as one list.
    var body = panel.querySelector('.chat-body') || log;

    function scrollDown() {
        body.scrollTop = body.scrollHeight;
    }

    function escapeHtml(s) {
        return String(s).replace(/[&<>"']/g, function (c) {
            return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c];
        });
    }

    // Bot copy may contain links, so it is trusted markup from our own
    // generator. Anything the visitor types is escaped.
    function addMessage(text, who) {
        var el = document.createElement('div');
        el.className = 'chat-msg ' + who;
        if (who === 'bot') {
            el.innerHTML = text;
        } else {
            el.textContent = text;
        }
        log.appendChild(el);
        scrollDown();
        return el;
    }

    function typing(callback) {
        var el = addMessage('…', 'bot');
        setTimeout(function () {
            el.remove();
            callback();
        }, 420);
    }

    function showTopicButtons() {
        replies.innerHTML = '';
        DATA.topics.forEach(function (t) {
            var b = document.createElement('button');
            b.type = 'button';
            b.textContent = t.label;
            b.addEventListener('click', function () {
                addMessage(t.label, 'user');
                replies.innerHTML = '';
                typing(function () {
                    addMessage(t.answer, 'bot');
                    showTopicButtons();
                });
            });
            replies.appendChild(b);
        });

        var human = document.createElement('button');
        human.type = 'button';
        human.textContent = DATA.humanLabel;
        human.addEventListener('click', function () {
            window.open(DATA.whatsapp, '_blank', 'noopener');
        });
        replies.appendChild(human);
    }

    // Score each topic by how many of its keywords appear in the question.
    // Longer keywords score higher, so "spare parts" beats a bare "parts".
    function findAnswer(question) {
        var q = question.toLowerCase();
        var best = null;
        var bestScore = 0;

        DATA.topics.forEach(function (t) {
            var score = 0;
            (t.keywords || []).forEach(function (k) {
                if (q.indexOf(k.toLowerCase()) !== -1) score += k.length;
            });
            if (score > bestScore) {
                bestScore = score;
                best = t;
            }
        });

        return bestScore > 0 ? best.answer : null;
    }

    function ask(question) {
        addMessage(question, 'user');
        replies.innerHTML = '';
        typing(function () {
            var answer = findAnswer(question);
            addMessage(answer || DATA.fallback, 'bot');
            showTopicButtons();
        });
    }

    form.addEventListener('submit', function (e) {
        e.preventDefault();
        var q = input.value.trim();
        if (!q) return;
        input.value = '';
        ask(q);
    });

    function openPanel() {
        panel.setAttribute('data-open', 'true');
        toggle.setAttribute('aria-expanded', 'true');
        document.body.classList.add('chat-open');
        if (!started) {
            started = true;
            addMessage(DATA.greeting, 'bot');
            showTopicButtons();
        }
        scrollDown();
        input.focus();
    }

    function closePanel() {
        panel.setAttribute('data-open', 'false');
        toggle.setAttribute('aria-expanded', 'false');
        document.body.classList.remove('chat-open');
        toggle.focus();
    }

    toggle.addEventListener('click', function () {
        if (panel.getAttribute('data-open') === 'true') closePanel();
        else openPanel();
    });

    closeBtn.addEventListener('click', closePanel);

    document.addEventListener('keydown', function (e) {
        if (e.key === 'Escape' && panel.getAttribute('data-open') === 'true') closePanel();
    });
})();
