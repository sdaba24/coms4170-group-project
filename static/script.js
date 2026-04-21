// A simple map for the titles
const roleTitles = {
    "att": "ATTACK",
    "mid": "MIDFIELD",
    "def": "DEFENSE"
};

// Player coordinate maps
const layouts = {
    "433": [
        {p: "GK", t: 45, l: 90, r: "def"},
        {p: "LB", t: 15, l: 72, r: "def"}, {p: "CB", t: 35, l: 72, r: "def"}, {p: "CB", t: 55, l: 72, r: "def"}, {p: "RB", t: 75, l: 72, r: "def"},
        {p: "CM", t: 25, l: 45, r: "mid"}, {p: "CDM", t: 45, l: 55, r: "mid"}, {p: "CM", t: 65, l: 45, r: "mid"},
        {p: "LW", t: 15, l: 15, r: "att"}, {p: "ST", t: 45, l: 10, r: "att"}, {p: "RW", t: 75, l: 15, r: "att"}
    ],
    "442": [
        {p: "GK", t: 45, l: 90, r: "def"},
        {p: "LB", t: 10, l: 72, r: "def"}, {p: "CB", t: 35, l: 72, r: "def"}, {p: "CB", t: 55, l: 72, r: "def"}, {p: "RB", t: 80, l: 72, r: "def"},
        {p: "LM", t: 10, l: 40, r: "mid"}, {p: "CM", t: 35, l: 40, r: "mid"}, {p: "CM", t: 55, l: 40, r: "mid"}, {p: "RM", t: 80, l: 40, r: "mid"},
        {p: "ST", t: 35, l: 15, r: "att"}, {p: "ST", t: 55, l: 15, r: "att"}
    ],
    "4231": [
        {p: "GK", t: 45, l: 90, r: "def"},
        {p: "LB", t: 10, l: 72, r: "def"}, {p: "CB", t: 35, l: 72, r: "def"}, {p: "CB", t: 55, l: 72, r: "def"}, {p: "RB", t: 80, l: 72, r: "def"},
        {p: "CDM", t: 35, l: 55, r: "mid"}, {p: "CDM", t: 55, l: 55, r: "mid"},
        {p: "LM", t: 10, l: 30, r: "mid"}, {p: "CAM", t: 45, l: 30, r: "mid"}, {p: "RM", t: 80, l: 30, r: "mid"},
        {p: "ST", t: 45, l: 10, r: "att"}
    ]
};

// Robust way to get formation ID from URL
const pathParts = window.location.pathname.split("/").filter(p => p !== "");
const formationKey = pathParts[pathParts.length - 1] || "433"; 

let formationsData = {};

// Use the data-json-url attribute we will set in HTML
const jsonUrl = document.body.getAttribute('data-json-url');

fetch(jsonUrl)
    .then(res => res.json())
    .then(data => {
        formationsData = data;
        initPitch();
    });

function initPitch() {
    const currentData = formationsData[formationKey];
    if (!currentData) return;

    resetInfoBox();

    const layout = layouts[formationKey] || layouts["433"];
    const layer = $("#player-layer");
    layer.empty();

    layout.forEach(player => {
        // Add specific role class (e.g., player-att) for highlighting
        const div = $(`<div class="player player-${player.r}" style="top:${player.t}%; left:${player.l}%;">${player.p}</div>`);
        
        div.on("click", function(e) {
            e.stopPropagation();
            $("#display-title").text(roleTitles[player.r]);
            $("#display-text").text(currentData.roles[player.r]);

            // Group Highlighting
            $(".player").removeClass("highlight-active");
            $(`.player-${player.r}`).addClass("highlight-active");
        });

        layer.append(div);
    });
}

$("#pitch").on("click", resetInfoBox);

function resetInfoBox() {
    const currentData = formationsData[formationKey];
    if (!currentData) return;
    
    $("#display-title").text(currentData.title);
    $("#display-text").text(currentData.description);
    $(".player").removeClass("highlight-active");
}

// Function to highlight the current formation in the banner
function highlightActiveLink() {
    // 1. Find all links inside the formation-bar
    const links = document.querySelectorAll('.formation-link');
    
    links.forEach(link => {
        // 2. Get the formation ID from the link's href (e.g., "433" from "/formations/433")
        const linkPath = link.getAttribute('href');
        const linkKey = linkPath.split('/').pop();

        // 3. If it matches our current formationKey, add the class
        if (linkKey === formationKey) {
            link.classList.add('active-link');
        } else {
            link.classList.remove('active-link');
        }
    });
}

// Call this function immediately
highlightActiveLink();