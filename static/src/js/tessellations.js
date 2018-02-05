const populateTessellations = () => {
    const BASE_URL = "http://pinaxproject.com/pinax-design/patches/"
    const BASE_REPO_URL = "http://github.com/pinax/"
    const WIDTH = 170;
    const HEIGHT = 186;
    const MARGIN = 20;
    const PADDING = 20;

    const calcPosition = (index, perRow, currentRow, currentY) => {
        let row = currentRow;
        let my = currentY;
        let mx = (index % perRow) * (WIDTH + MARGIN) + PADDING;

        if (index > 0 && index % perRow === 0) {
            row += 1;
            my += (HEIGHT + MARGIN) - (HEIGHT / 4);
        }
        if (row % 2 === 0) {
            mx += (WIDTH + MARGIN) / 2;
        }
        return {mx, my, row};
    }

    // loop through all class="tessellation" elements
    var elements = document.getElementsByClassName("tessellation");
    for (var i = 0, len = elements.length; i < len; i++) {
        const tess = elements[i];
        const apps = $(tess).data("apps").split(' ');
        const itemsPerRow = parseInt($(tess).data("perRow"));

        let row = 1;
        let x = 0 + PADDING;
        let y = 0 + PADDING;

        for (let i=0; i<apps.length; i++) {
            const position = calcPosition(i, itemsPerRow, row, y);
            y = position.my;
            row = position.row;

            const repoUrl = `${BASE_REPO_URL}${apps[i]}/`;
            var anchor = document.createElement('a');
            anchor.href = repoUrl;

            const imageSrcUrl = `${BASE_URL}${apps[i]}.svg`;
            const $img = document.createElement('img');
            $img.setAttribute('style', `left:${position.mx}px; top:${position.my}px`);
            $img.setAttribute('src', imageSrcUrl);
            $img.setAttribute('title', apps[i]);
            $img.setAttribute('data-toggle', "tooltip");

            anchor.appendChild($img);
            $(tess).append(anchor);
        }
        $(tess).css({
           width: `${(PADDING * 2) + ((WIDTH + MARGIN) * itemsPerRow) - MARGIN}px`,
           height: `${(PADDING * 2) + ((HEIGHT) * row) - ((HEIGHT / 8) * (row - 1)) - 3}px`  // don't get the -3px
        });
    }
};

export default populateTessellations;
