import asyncio
from typing import Literal
from playwright.async_api import async_playwright

async def crawl_luck(gender : Literal["남성", "여성"], 
                     birth_type : Literal["양력", "음력 평달", "음력 윤달"], 
                     birth_time_code : Literal["0", "1", "2", "3", "4", "5","6", "7", "8", "9", "10", "11", "12"],
                     birth_year : str,
                     birth_month : str,
                     birth_day : str,
                     ):
    print("▶ Playwright 시작")

    if gender == '여성' : 
        gender_code = 'f'
    else : 
        gender_code = 'm'
    
    if birth_type == '양력' : 
        birth_type_eng = 'solar'
    elif birth_type == '음력 평달' : 
        birth_type_eng = 'lunarGeneral'
    else : 
        birth_type_eng = 'lunarLeap'



    async with async_playwright() as p:

        try : 
            print("▶ 브라우저 실행 중...")
            browser = await p.chromium.launch(headless=True)
            page = await browser.new_page()

            print("▶ 네이버 운세 페이지 접속 중...")
            await page.goto("https://search.naver.com/search.naver?query=오늘의+운세")
            await page.wait_for_timeout(5000)  # 5초 대기 (필요 시 늘릴 수 있음)

            print("▶ 성별 드롭다운 열기")
            await page.click("#fortune_birthCondition > div.tb_box > div.system_select_box > div.gender._togglePanelSelect > div > a")  # 드롭다운 열기


            # 드롭다운 애니메이션 등으로 인해 요소가 숨겨진 상태일 수 있으니 대기 추가
            await page.wait_for_timeout(1000)  # 1초 대기 (필요 시 늘릴 수 있음)

            # await page.screenshot(path="step1_open_gender_select.png", full_page=True)

            # 선택 옵션이 표시되는지 확인 후 클릭
            print(f"▶ 성별 선택: {gender}")
            await page.evaluate(f'''
                const el = document.querySelector("#fortune_birthCondition > div.tb_box > div.system_select_box > div.gender._togglePanelSelect li[data-kgs-option='{gender_code}']");
                el?.scrollIntoView({{ behavior: 'instant', block: 'center' }});
            ''')
            await page.click(f"#fortune_birthCondition > div.tb_box > div.system_select_box > div.gender._togglePanelSelect li[data-kgs-option='{gender_code}'] a", force=True)

            print(f"▶ {birth_type} 선택")
            await page.evaluate("""
                const trigger = document.querySelector(".year ._trigger");
                if (trigger) trigger.click();
            """)
            await page.wait_for_selector(f"li.group_item[data-kgs-option='{birth_type_eng}'] a", state="visible")
            await page.click(f"li.group_item[data-kgs-option='{birth_type_eng}'] a")           

            print("▶ 태어난 시 선택")
            await page.evaluate("""
                const trigger = document.querySelector(".time ._trigger");
                if (trigger) trigger.click();
            """)
            # 묘시 항목을 스크롤로 가운데로 가져오기
            await page.evaluate(f"""
                const el = document.querySelector("li.group_item[data-kgs-option='{birth_time_code}']");
                el?.scrollIntoView({{ behavior: 'instant', block: 'center' }});
            """)
            await page.wait_for_selector(f"li.group_item[data-kgs-option='{birth_time_code}'] a", state="visible")
            await page.click(f"li.group_item[data-kgs-option='{birth_time_code}'] a")     


            # await page.screenshot(path="step1_gender_birthtype_birthtime_selection.png", full_page=True)

            print("▶ 생년월일 선택창 열기 클릭")
            await page.click(".select_pop._trigger")

            # 연도 선택
            print("▶ 연도 항목 스크롤 + 클릭")
            await page.evaluate(f"""
                const el = document.querySelector("#fortune_birthCondition > div.tb_box > div.pop_select_box._dateCustomSelect > div > div.mod_select_option > div > div:nth-child(1) li.item._li[data-value='{birth_year}']");
                el?.scrollIntoView({{ behavior: 'instant', block: 'center' }});
            """)
            await page.wait_for_timeout(500)
            await page.click(f"#fortune_birthCondition > div.tb_box > div.pop_select_box._dateCustomSelect > div > div.mod_select_option > div > div:nth-child(1) li.item._li[data-value='{birth_year}'] a", force=True)

            # 월 선택
            print("▶ 월 항목 스크롤 + 클릭")
            await page.evaluate(f"""
                const el = document.querySelector("#fortune_birthCondition > div.tb_box > div.pop_select_box._dateCustomSelect > div > div.mod_select_option > div > div:nth-child(2) li.item._li[data-value='{birth_month}']");
                el?.scrollIntoView({{ behavior: 'instant', block: 'center' }});
            """)
            await page.wait_for_timeout(500)
            await page.click(f"#fortune_birthCondition > div.tb_box > div.pop_select_box._dateCustomSelect > div > div.mod_select_option > div > div:nth-child(2) li.item._li[data-value='{birth_month}'] a", force=True)

            # 일 선택
            print("▶ 일 항목 스크롤 + 클릭")
            await page.evaluate(f"""
                const el = document.querySelector("#fortune_birthCondition > div.tb_box > div.pop_select_box._dateCustomSelect > div > div.mod_select_option > div > div:nth-child(3) li.item._li[data-value='{birth_day}']");
                el?.scrollIntoView({{ behavior: 'instant', block: 'center'}});
            """)
            await page.wait_for_timeout(500)
            await page.click(f"#fortune_birthCondition > div.tb_box > div.pop_select_box._dateCustomSelect > div > div.mod_select_option > div > div:nth-child(3) li.item._li[data-value='{birth_day}'] a", force=True)

            selected_date = await page.locator(".birth_date._trigger_text").inner_text()
            print(f"✅ 선택된 생년월일: {selected_date}")

            # await page.screenshot(path="step2_after_date_selection.png", full_page=True)

            print("▶ '운세 확인하기' 버튼 클릭")
            await page.click(".img_btn._resultBtn")

            print("▶ 총운 결과 대기 중...")
            await page.wait_for_selector("dl.infor._innerPanel")

            print("▶ 총운 결과 텍스트 추출")
            sections = await page.locator("dl.infor._innerPanel").all()
            for i, section in enumerate(sections[:1]): # 오늘의 운세만 보려고
                title = await section.locator("strong").text_content()
                desc = await section.locator("p").text_content()
                # print(f"\n[{i+1}] {title}\n{desc}")

            print("✅ 크롤링 완료!")
            await page.screenshot(path="result.png", full_page=True)
            print(f"\n🎯 오늘의 총운: {title}\n{desc}")

            return {
                "total_luck" : title,
                "discription" : desc
            }
        
        except Exception as e :
            print("🚫 ERROR!! :", e) 
            await page.screenshot(path="error.png", full_page=True)

        finally :
            await browser.close()
