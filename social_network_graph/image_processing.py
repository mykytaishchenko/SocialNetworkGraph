from PIL import Image, ImageDraw, ImageOps
import matplotlib.pyplot as plt


def add_images_on_graph(graph, pos: dict, ax) -> None:
    fig = plt.gcf()

    trans = ax.transData.transform
    trans2 = fig.transFigure.inverted().transform

    for n in graph.nodes():
        (x, y) = pos[n]
        x, y = trans((x, y))  # figure coordinates
        x, y = trans2((x, y))  # axes coordinates

        size = graph.nodes[n]['size']
        img = graph.nodes[n]['image']
        a = plt.axes([x - size / 2.0, y - size / 2.0, size, size])
        a.imshow(img)
        a.set_aspect('equal')
        a.axis('off')


def round_image(img: Image) -> Image:
    mask = Image.new('L', img.size)
    draw = ImageDraw.Draw(mask)
    draw.ellipse((0, 0) + img.size, fill=255)

    img = ImageOps.fit(img, mask.size, centering=(0.5, 0.5))
    img.putalpha(mask)
    img.thumbnail(img.size, Image.ANTIALIAS)
    return img
