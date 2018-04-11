from pptx import Presentation
from pptx.util import Cm,Pt
from django.conf import settings
import os


def generate_ppt(product_list, path):
    """
    生成PPT
    :param product_list: 商品列表
    :return:
    """
    prs = Presentation()
    blank_slide_layout = prs.slide_layouts[6]

    for product in product_list:
        slide = prs.slides.add_slide(blank_slide_layout)

        # 主图
        left = Cm(1.32)
        top = Cm(1.59)
        width = Cm(10.58)
        height = Cm(10.58)

        slide.shapes.add_picture(os.path.join(settings.BASE_DIR, product.images.first().productimage.path) , left, top, width, height)
        #

        # 小图
        start_left = Cm(1.32)
        start_top = Cm(10.58 + 1.59)
        width=height = Cm(2.65)
        i = 0
        for image in product.images.all()[1:4]:
            slide.shapes.add_picture('coach.jpg', Cm(1.32 + i * 2.65), start_top, width, height)
            i = i + 1
        #

        # 描述
        desc_box = slide.shapes.add_textbox(Cm(10.58 + 1.32), Cm(1.59 + 1.59), Cm(13.23), Cm(7.14))
        tf = desc_box.text_frame
        tf.clear()
        p = tf.paragraphs[0]
        p.text = "品牌：{}".format(product.brand.name)
        p.font.bold = False
        p.font.size = Pt(14)

        p = tf.add_paragraph()
        p.text = ""
        p.font.bold = False
        p.font.size = Pt(14)

        product_items = product.productItems.order_by("price").all()
        start_price = product_items.first().price
        end_price = product_items.last().price

        p = tf.add_paragraph()
        if start_price == end_price:
            p.text = "单价：{} 元".format(start_price)
        else:
            p.text = "单价：{} - {} 元".format(start_price, end_price)
        p.font.bold = False
        p.font.size = Pt(14)

        title_box = slide.shapes.add_textbox(Cm(10.58 + 1.32), Cm(1.59 + 1.59 + 7.14), Cm(13.23), Cm(0.79))
        tf = title_box.text_frame
        tf.clear()
        p = tf.paragraphs[0]
        p.text = "产品简介："
        p.font.bold = True
        p.font.size = Pt(16)

        desc_box = slide.shapes.add_textbox(Cm(10.58 + 1.32), Cm(1.59 + 1.59 + 7.14 + 0.79), Cm(13.23), Cm(5.29))
        tf = desc_box.text_frame
        tf.word_wrap = True
        tf.clear()
        p = tf.paragraphs[0]
        p.text = "TODO:待定"
        p.font.bold = False
        p.font.size = Pt(14)

    prs.save(path)
