# 设置为UTF8编码格式，防止中文乱码
# -*- coding: utf-8 -*-
import utils
from DrissionPage import ChromiumPage
import base64
import os



def get_logo_by_keyword(page, keyword):
    url = f'https://ai.gameba.cc/q/?query={keyword}'
    page.get(url=url)
    logoEle = page.ele('.lazy unfancybox loaded', timeout=3)
    if not logoEle:
        print(f'!!! Error: 未找到Logo资源: {keyword}')
    else:
        logoImgSaveFile = f'./logo/logo-{keyword}.png'
        print(f'>>> Logo图片保存中...文件名: {logoImgSaveFile}')
        if os.path.exists(logoImgSaveFile):
            os.remove(logoImgSaveFile)
        logoEle.save(path='./logo/', name=f'logo-{keyword}.png', timeout=3)


if __name__ == '__main__':

    logoNames = [
        "Kimi",
        "Chatdoc",
        "ReadPaper",
        "跃问",
        "智谱清言",
        "Timtalk",
        "豆包",
        "Al Financial Report Expert",
        "Microsoft Copilot for Finance",
        "秘塔AI",
        "Scholar GPT",
        "得到学习助手",
        "360AI",
        "天工AI",
        "perplexity",
        "通义千问",
        "文心一言",
        "稿定AI",
        "美图",
        "爱设计",
        "图宇宙智能设计",
        "画宇宙AI商品图",
        "Whop唯象妙境",
        "无界AI",
        "LiblibAI",
        "WPS AI",
        "腾讯文档",
        "讯飞智文",
        "AiPPT",
        "Gamma",
        "GitHub Copilot",
        "CodeGeeX",
        "Moka Eva",
        "扣子",
        "钉钉",
        "Dify",
        "讯飞写作",
        "火山写作",
    ]

    # 创建页面对象，接管该端口号已经打开的浏览器，从而继续使用浏览器的登录态继续操作
    page = ChromiumPage()


    for logoName in logoNames:
        get_logo_by_keyword(page, logoName)

