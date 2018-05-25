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

        # logo
        slide.shapes.add_picture(os.path.join(settings.BASE_DIR, product.brand.logo.path), Cm(0), Cm(0), Cm(5.58), Cm(3.62))
        #

        # 主图
        left = Cm(1.59)
        top = Cm(2.98)
        width = Cm(10.92)
        height = Cm(15.29)

        slide.shapes.add_picture(os.path.join(settings.BASE_DIR, product.images.first().productimage.path) , left, top, width, height)
        #

        # 描述
        desc_box = slide.shapes.add_textbox(Cm(14.29), Cm(2.78), Cm(8.33), Cm(1.32))
        tf = desc_box.text_frame
        tf.clear()
        p = tf.paragraphs[0]
        p.text = "{}".format(product.name)
        p.font.bold = True
        p.font.name = 'Microsoft YaHei'
        p.font.size = Pt(28)

        # 价格
        price_box = slide.shapes.add_textbox(Cm(14.29), Cm(4.11), Cm(6.15), Cm(2.82))
        tf = price_box.text_frame
        tf.clear()
        product_items = product.productItems.order_by("price").all()
        start_price = product_items.first().price
        end_price = product_items.last().price

        p = tf.paragraphs[0]
        p.font.name = 'Microsoft YaHei'
        if start_price == end_price:
            p.text = "市场价：{} 元".format(start_price)
        else:
            p.text = "市场价：{} - {} 元".format(start_price, end_price)
        p.font.bold = True
        p.font.size = Pt(15)
        #

        # 规格添加
        details_box = slide.shapes.add_textbox(Cm(14.29), Cm(4.66), Cm(6.15), Cm(2.82))
        tf = details_box.text_frame
        tf.clear()

        p = tf.add_paragraph()

        # 开始添加规格描述：格式为：颜色：红 黄
        specname_array = product.attributes
        spec_desc_text = ''
        for spec_name in specname_array:
            text_row = '{}:'.format(spec_name)
            for sku in product.productItems.all():
                text_row = text_row + sku.attributes.get(spec_name) + ' '
            spec_desc_text = spec_desc_text + text_row + '\n'
            #p = tf.add_paragraph()
        p.font.bold = False
        p.font.size = Pt(15)
        p.text = spec_desc_text
        p.line_spacing = 1.5
        #


        title_box = slide.shapes.add_textbox(Cm(14.29), Cm(8.37), Cm(11.47), Cm(11.11))
        tf = title_box.text_frame
        tf.word_wrap = True
        tf.clear()
        p = tf.paragraphs[0]
        p.font.name = 'Microsoft YaHei'
        p.text = "产品卖点："
        p.font.bold = True
        p.font.size = Pt(11)
        p = tf.add_paragraph()
        p.font.bold = False
        p.font.size = Pt(11)
        p.font.name = 'Microsoft YaHei'
        p.text = product.simple_description
        p.line_spacing = 1.5

        """
        desc_box = slide.shapes.add_textbox(Cm(10.58 + 1.32), Cm(1.59 + 1.59 + 7.14 + 0.79), Cm(13.23), Cm(5.29))
        tf = desc_box.text_frame
        tf.word_wrap = True
        tf.clear()
        p = tf.paragraphs[0]
        p.text = "TODO:待定"
        p.font.bold = False
        p.font.size = Pt(14)
        """

    if not os.path.exists(os.path.dirname(path)):
        os.makedirs(os.path.dirname(path))
    prs.save(path)
