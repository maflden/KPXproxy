def get_kpx_data_via_gas():
    # 새로 배포한 구글 웹 앱 URL
    GAS_WEBAPP_URL = "https://script.google.com/macros/s/AKfycbwG0l-vttmHkuys0eMlFnuIT6vzcIV3pAnOoka4VcEe0-80zK7zjLgN6HCrK6KXQhVX/exec"
    
    try:
        # 타임아웃을 30초로 늘림 (구글이 재시도하는 시간까지 고려)
        response = requests.get(GAS_WEBAPP_URL, timeout=30)
        
        # 만약 구글 스크립트에서 에러 메시지를 보냈다면
        if "Error:" in response.text:
            st.warning("KPX 서버 응답이 지연되고 있습니다. 잠시 후 자동으로 다시 시도합니다.")
            return None
            
        root = ET.fromstring(response.content)
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
    except requests.exceptions.Timeout:
        st.error("데이터 수신 시간이 초과되었습니다. 네트워크 상태를 확인하세요.")
    except Exception as e:
        st.error(f"알 수 없는 오류 발생: {e}")
    return None
