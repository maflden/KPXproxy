import streamlit as st
import requests
import xml.etree.ElementTree as ET
import pandas as pd
from datetime import datetime

# 1. API 정보 설정
KPX_SERVICE_KEY = "11d07546d5cc1d813529086db2074456e7567d7f15e13e2e4357e5f22a81495a"
# 실제 호출할 KPX URL
target_url = f"https://openapi.kpx.or.kr/openapi/sukub5mMaxDatetime/getSukub5mMaxDatetime?serviceKey={KPX_SERVICE_KEY}"

# 2. CORS 및 IP 차단 우회를 위한 공용 프록시 목록
# 하나가 안될 경우를 대비해 여러 프록시 서버를 경유하도록 구성할 수 있습니다.
proxy_urls = [
    f"https://api.allorigins.win/get?url={requests.utils.quote(target_url)}",
    f"https://corsproxy.io/?{requests.utils.quote(target_url)}"
]

def get_realtime_power_data():
    for url in proxy_urls:
        try:
            # 프록시 서버를 통해 데이터 요청
            response = requests.get(url, timeout=15)
            
            if response.status_code == 200:
                # 프록시 서버마다 응답 형식이 다름 (allorigins는 json안에 contents로 들어옴)
                if "allorigins" in url:
                    content = response.json()['contents']
                else:
                    content = response.text
                
                # XML 파싱
                root = ET.fromstring(content)
                item = root.find('.//item')
                
                if item is not None:
                    return {
                        "suppAbility": item.findtext('suppAbility'),
                        "currPwrTot": item.findtext('currPwrTot'),
                        "forecastLoad": item.findtext('forecastLoad'),
                        "suppReservePwr": item.findtext('suppReservePwr'),
                        "suppReserveRate": item.findtext('suppReserveRate'),
                        "operReservePwr": item.findtext('operReservePwr'),
                        "operReserveRate": item.findtext('operReserveRate'),
                        "baseDatetime": item.findtext('baseDatetime')
                    }
        except Exception as e:
            continue # 실패하면 다음 프록시로 시도
            
    return None

# 3. Streamlit UI 출력
st.title("⚡ 실시간 전력수급 현황 (직접 우회 방식)")

data = get_realtime_power_data()

if data:
    # 데이터 출력 부분
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("현재 수요", f"{float(data['currPwrTot']):,.0f} MW")
    with col2:
        st.metric("공급 능력", f"{float(data['suppAbility']):,.0f} MW")
    with col3:
        st.metric("예비율", f"{data['suppReserveRate']}%")
        
    st.info(f"기준 시간: {data['baseDatetime']}")
else:
    st.error("모든 우회 경로가 차단되었거나 KPX 서버 응답이 없습니다. 잠시 후 다시 시도해 주세요.")
