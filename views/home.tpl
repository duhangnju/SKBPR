<div>
    <h2>Suggested queries:</h2>
% for query in queries:
    <a class="query-trigger" href="#">{{ query }}</a><br>
% end
</div>

<h2>Suggested Items:</h2>
<ul id="suggestions">
</ul>

<script src="/static/jquery-2.0.1.min.js"></script>
<script src="/static/home.js"></script>
