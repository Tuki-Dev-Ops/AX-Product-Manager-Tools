# 다브랜드 F&B 본사 관리 시스템 기능 범위 조사

조사일 2026-09-04. 상용 제품이 공통으로 제공하는 기능을 확인해 우리 서비스의 범위를 정하기 위한 조사다.

## 근거 수준

| 제품 | 근거 |
| --- | --- |
| Toast | 공식 플랫폼 가이드, 개발자 문서, 고객센터 직접 확인 |
| Square | 공식 고객센터, 개발자 레퍼런스 직접 확인 |
| Lightspeed Restaurant K-Series | 공식 고객센터 직접 확인 |
| Flipdish | 공식 개발자 문서 직접 확인 |
| Olo | 제품 페이지 확인. 도움말센터 접근 차단 |
| 배달의민족 프랜차이즈 | 도움말 검색 결과. 본문 접근 차단 |
| 토스플레이스 | 공식 안내 문서 직접 확인 |
| 페이히어 | 언론 기사만 확인 |
| 오케이포스, 유어오더, 먼슬리키친 | 미확인 |

## 기능 제공 현황

O 공식 문서 확인, △ 부분 확인, - 확인되지 않음

| 기능 | Toast | Square | Lightspeed | Olo | Flipdish | 배민 | 토스플레이스 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 본사 메뉴 마스터 | O | O | O | O | O | O | O |
| 매장별 가격 재정의 | O | O | O | △ | △ | - | - |
| 채널별 메뉴·가격 | △ | O | - | O | O | - | - |
| 시간대별 가격 | O | △ | - | - | - | - | - |
| 품절 관리 | O | O | - | O | O | O | - |
| 메뉴 배포(발행) | O | △ | O | O | O | O | △ |
| 매장 개설 | O | O | O | - | O | - | O |
| 계정·권한 분리 | O | O | △ | - | - | O | O |
| 매장 그룹 비교 | O | O | - | - | - | - | - |
| 한시 매장 전용 기능 | - | - | △ | - | - | - | - |
| 행사 단위 기간 그룹 | - | - | - | - | - | - | - |
| 공개 API | O | O | △ | △ | O | - | - |

## 1. 메뉴 마스터 전달 방식

실시간 조회 방식은 어느 제품에서도 확인되지 않았다. 확인된 방식은 둘이다.

### 본사 발행 후 전송

Toast는 저장과 발행을 분리한다. 변경을 저장해도 발행 전까지 단말과 API 결과에 반영되지 않는다. 다매장은 발행 설정 화면에서 대상 매장을 선택해 발행한다. 매장별 마지막 발행 시각을 표시한다. 예약 발행을 지원한다. 롤백은 제공하지 않으며 값을 수동으로 되돌린 뒤 재발행하도록 안내한다.

- https://doc.toasttab.com/doc/platformguide/platformPublishingOverview.html
- https://doc.toasttab.com/doc/platformguide/publishingChangesForMultipleLocations.html

Lightspeed는 메뉴를 생성한 매장에서만 수정할 수 있고, 변경 후 메뉴 갱신 또는 단말 리로드를 선택해 반영한다.

- https://k-series-support.lightspeedhq.com/hc/en-us/articles/4755505361947-Sharing-menus-with-business-locations

Flipdish는 메뉴에 리비전을 두고 특정 리비전을 판매 채널에 발행한다. 발행 상태 조회를 별도 제공한다.

- https://developers.flipdish.com/llms.txt

### 주기적 내려받기

Olo는 POS 연동 매장의 가격을 POS에서 끌어오며 매일 두 차례 자동 갱신한다.

- https://olosupport.zendesk.com/hc/en-us/articles/115000632506-Running-the-Price-Updater

### 네트워크 불안정 환경

Toast는 연결이 끊기면 오프라인 모드로 전환하고 40초 후 단말에 배너를 표시한다. 오프라인 중 주문은 단말에 로컬 저장되며 다른 단말에서 보이지 않는다. 현금과 카드 결제는 가능하고 기프트카드, 적립 사용, 고객 크레딧은 불가하다. 연결 복구 시 자동 동기화한다.

로컬 동기화 모드는 유선 연결된 단말 하나를 로컬 허브로 지정한다. 허브는 단말 간 주문 전달, 주방 표시, 결제, 영수증 출력을 중계한다. 매장당 1대다.

- https://doc.toasttab.com/doc/platformguide/adminOfflineModeOverview.html
- https://doc.toasttab.com/doc/platformguide/platformOfflineModeLocalSync.html

## 2. 매장별 가격 재정의

| 제품 | 재정의 단위 |
| --- | --- |
| Toast | 기본가, 사이즈별, 메뉴별, 매장별, 시간대별, 오픈 프라이스, 가격 레벨 |
| Square | 매장별. 여러 매장 일괄 적용. 대시보드에서만 설정 가능 |
| Lightspeed | 상품 공유 상태를 Local, Shared, Global로 구분. Shared는 이름만 공유하고 가격은 매장별로 변경 |
| Flipdish | Price band를 조직 단위로 정의. 베타 |
| Olo | POS 연동 시 POS 가격 사용. 미연동 시 매장 화면에서 입력 |

- https://doc.toasttab.com/doc/platformguide/platformMenuManagerWorkingWithMenuItems.html
- https://squareup.com/help/us/en/article/8242-create-item-price-overrides-for-multiple-locations-in-square-dashboard

Toast에는 제약이 있다. 버전이 나뉜 메뉴 항목이라도 매장별 가격은 같은 값을 공유한다. 가격 재정의 축과 메뉴 구성 버전 축이 분리되어 있지 않다.

## 3. 품절의 주체와 충돌

주체는 매장이다. 조사한 모든 제품이 품절을 매장 단위 상태로 관리한다.

Square는 품절을 읽기 전용 값으로 두고 재고 소진 또는 판매자 조작으로 설정한다. 재판매 시각을 지정할 수 있다. 두 값 모두 매장별 재정의 객체에 속한다.

- https://developer.squareup.com/reference/square/objects/ItemVariationLocationOverrides

배달의민족은 축을 분리한다. 매장은 가게메뉴판에서 자유롭게 품절을 처리한다. 본사가 여러 매장의 메뉴를 일괄로 숨기려면 별도 접수 절차를 거친다.

- https://woowahan.zendesk.com/hc/ko/articles/4415853397529-본사메뉴판과-가게메뉴판-차이점

충돌 처리 규칙은 어느 제품 문서에서도 확인되지 않았다. 대신 충돌을 만들지 않는 설계가 확인된다. 본사는 메뉴의 존재와 노출을 결정하고 매장은 당일 판매 가능 여부를 결정한다. 두 값이 별개 필드다.

## 4. 본사와 가맹점의 권한 경계

Toast는 메뉴 항목마다 소유자와 대상을 둔다. 소유자는 편집 권한자를, 대상은 그 버전을 사용할 매장 또는 매장 그룹을 지정한다. 대상은 소유자와 같거나 그 하위여야 한다. 매장 그룹은 계층을 가진다.

- https://doc.toasttab.com/doc/platformguide/platformMenuManagerMenuAndMultiLocationRestaurants.html

토스플레이스는 데이터 종류로 경계를 나눈다. 본사는 점주 동의 없이 상품을 사전 등록할 수 있다. 매출 조회는 점주 동의가 있어야 가능하다.

- https://toss.oopy.io/1d9714bb-fde7-805d-a72e-cd14c8e20b2c

공통 경계는 다음과 같다.

| 구분 | 본사 | 가맹점 |
| --- | --- | --- |
| 메뉴 생성·삭제 | 가능 | 불가 |
| 메뉴명·이미지·구성 | 가능 | 불가 |
| 매장별 노출 여부 | 가능 | 제품별로 다름 |
| 가격 | 가능 | 제품별로 다름 |
| 품절 | 일괄 숨김만 | 가능 |
| 영업시간 | 불가 | 가능 |
| 단말 설정 | 불가 | 가능 |
| 매출 조회 | 동의 또는 계약 범위 | 자기 매장 |

## 5. 한시 매장과 기간 단위 그룹

세 가지로 나뉜다.

### 한시 매장 유형은 없다

Lightspeed는 팝업 매장 운영 문서를 제공하지만 시스템상 별도 유형이 아니다. 계정 매니저에게 연락해 매장 수 한도를 늘리고, 종료 시에도 연락해 비활성화한다. 재고는 수동 이관하고 수동 회수한다.

- https://retail-support.lightspeedhq.com/hc/en-us/articles/10122796017179-Opening-a-pop-up-shop

Square는 매장을 삭제할 수 없고 비활성화만 가능하다. 임시 매장 개념이 문서에 없다.

### 매장 그룹 비교는 있다

Toast는 매장 그룹을 직접 만든다. 용도로 브랜드별 묶기, 부가 제품 단위 관리, 리포팅 그룹 구성을 제시한다.

- https://support.toasttab.com/en/article/location-groups

Square for Franchises도 매장 그룹을 제공하며 하위 그룹까지 계층을 만들 수 있다.

- https://squareup.com/help/us/en/article/8120-manage-your-square-for-franchises-location-groups

### 기간이 정해진 행사 단위 그룹 비교는 없다

Toast 매장 그룹에는 기간 속성이 없다. 아카이브 상태만 있다. Square 매장 그룹도 기간 개념이 없다. Toast 벤치마킹의 다지점 비교는 계정에 이미 있는 다지점 구조를 전제하며 필터 차원은 매장, 기간, 주문 채널, 동종 업계 기준이다.

- https://support.toasttab.com/en/article/Toast-Benchmarking-Multi-Unit-Group-Overview

상권 단위 그룹 비교는 선례가 있다. 특정 기간에 열린 여러 매장을 하나의 행사로 묶어 다른 행사와 비교하는 기능은 확인되지 않았다. 상용 제품은 매장을 영구 개설물로 전제한다.

## 6. 공개 API

| 제품 | 제공 항목 | 인증 |
| --- | --- | --- |
| Toast | 주문, 메뉴, 인력, 매장 설정, 재고, 파트너. 재고는 품절과 수량 지정 항목만 반환. 재고 웹훅 제공 | OAuth2 client credentials |
| Square | Catalog API, Locations API. 매장별 재정의 객체에 가격, 재고 추적, 품절, 재판매 시각 필드 | OAuth. 읽기와 쓰기 권한 분리 |
| Flipdish | 메뉴 생성·수정·발행·리비전, 조직과 매장과 판매 채널 관리, 품절, 판매와 주문 분리, 웹훅 구독 | OAuth2 client credentials. IP당 60초 50회 제한 |
| Olo | 마켓플레이스와 메뉴, 가격, 매장 정보, 품목 가용성 양방향 동기화 | 미확인 |
| 국내 제품 | 미확인 | 미확인 |

- https://doc.toasttab.com/doc/devguide/authentication.html
- https://developers.flipdish.com/docs/api-overview.md

외부에 메뉴와 매장을 제공할 때의 사실상 표준은 OAuth2 client credentials다.

## 8. Lightspeed, Olo, Flipdish 상세

세 제품의 공식 도움말과 개발자 문서를 직접 확인한 결과다. Olo 개발자 포털은 파트너 인증이 걸려 있어 접근하지 못했다.

### 본사 통제력

통제력은 Olo, Flipdish, Lightspeed 순으로 강하다.

Olo만 본사 메뉴를 명시적 마스터로 정의한다. 카테고리와 상품은 본사 메뉴에서만 만들고, 매장 메뉴는 그 항목을 켜고 끄는 계층이다. 상품마다 매장이 원가를 바꿀 수 있는지 지정하는 값을 둔다. 본사가 항목 단위로 매장 수정 권한을 통제한다.

- https://olosupport.zendesk.com/hc/en-us/articles/360025658332-Part-1-Company-Menu-Admin

Flipdish는 소유자가 메뉴를 잠글 수 있다. 매장 역할은 기본이 조회 전용이고 필요할 때 편집 권한을 준다. 변경 이력을 담당자별로 남긴다.

- https://help.flipdish.com/en/articles/9585362-teammate-permissions-overview

Lightspeed는 본사 계층 자체가 없다. 동등한 매장 집합이고 전환 메뉴로 이동한다. 통제는 상품 공유 상태로만 한다. 필드 단위 잠금이 없고 상태 변경이 단방향이다.

- https://k-series-support.lightspeedhq.com/hc/en-us/articles/23973504428059-Navigating-business-locations

### 품절 자동 해제

세 제품 모두 시간 지정 후 자동 복귀를 제공한다.

| 제품 | 방식 |
| --- | --- |
| Lightspeed | 1시간, 12시간, 24시간, 무기한 중 선택. 기간 종료 시 자동 복귀 |
| Flipdish | 시간 단위로 지정. 배차 유형, 판매 채널별로 구분해 적용 |
| Square | 재판매 시각을 값으로 지정 |

- https://k-series-support.lightspeedhq.com/hc/en-us/articles/10724827631259-Setting-up-and-using-Item-availability
- https://help.flipdish.com/en/articles/9585210-hide-snooze-a-property-temporarily-on-your-flipdish-pos

Flipdish는 유효한 단말 비밀번호를 가진 직원이면 누구나 품절을 실행할 수 있다. 현장 권한이다.

### 단말 반영

세 제품 모두 발행 후 단말 반영에 재시작이나 갱신 동작이 개입한다.

Lightspeed는 백오피스 변경이 단말에 자동 전파되지 않는다고 명시한다. 단말 상태를 연결됨, 백그라운드, 끊김으로 표시하고 동기화 상태를 정상, 갱신 필요, 원격 갱신 요청됨으로 구분한다.

Flipdish는 발행 후 단말을 재시작해 최신 메뉴를 받으라고 안내한다. 발행 상태를 판매 채널별로 조회할 수 있고 진행 중인 발행을 취소할 수 있다.

Olo는 외부 마켓플레이스에 웹훅으로 알린 뒤 상대가 가져가는 방식이다. 즉시 반영을 보장하지 않는다.

- https://k-series-support.lightspeedhq.com/hc/en-us/articles/1260804658149-Managing-POS-devices
- https://help.flipdish.com/en/articles/9969879-how-to-manage-your-menu-with-3rd-party-order-management

### 오프라인 동작

Lightspeed도 오프라인 문서를 따로 둔다. 인터넷이 끊기면 로컬 네트워크로 주문을 계속 받고, 지정된 단말이 필요한 데이터를 보관했다가 복구 시 전송한다. 로컬 네트워크까지 끊기면 그 단말만 동작한다.

- https://k-series-support.lightspeedhq.com/hc/en-us/articles/53028167251867-Offline-POS-functionality

### 한시 매장

Lightspeed, Olo, Flipdish 모두 임시 매장 개념이 문서에 없다. 매장은 영구 객체다.

Lightspeed의 팝업 문서는 소매 제품에만 있고 외식 제품에는 없다. 그마저 일반 매장을 추가하고 제거하는 절차다. Olo와 Flipdish는 매장 삭제가 불가능하고 종료 상태나 영업시간 조정으로만 대응한다.

혼동하기 쉬운 개념이 둘 있다. 하나는 가상 브랜드다. 같은 주방에서 여러 브랜드를 운영하는 방식이며 임시 매장이 아니다. 다른 하나는 기간 한정 판매다. 상품 단위이지 매장 단위가 아니다.

### 매장 그룹 비교

Toast와 Square는 저장 가능한 매장 그룹을 제공한다. Lightspeed, Olo, Flipdish는 제공하지 않는다.

Lightspeed는 개인 전용 리포트 설정 저장이 가장 근접하다. 리포트당 10개까지이고 공유할 수 없다. Olo는 리포트를 실행할 때마다 매장을 고른다. Flipdish의 채널 그룹은 통화 공유와 소비자용 매장 찾기 목적이다.

- https://k-series-support.lightspeedhq.com/hc/en-us/articles/49181138716699-Managing-custom-report-views

### 외부 연동 인증

| 제품 | 인증 |
| --- | --- |
| Toast | OAuth2 client credentials |
| Flipdish | OAuth2 client credentials. 웹훅에 서명 검증, 자동 재시도, 멱등성 헤더 제공 |
| Lightspeed K-Series | OAuth2 authorization code. 다른 방식은 지원하지 않는다고 명시. 접근 토큰 25분, 갱신 토큰 40일 |
| Olo | 파트너 인증 필요. 확인하지 못함 |

- https://api-portal.lsk.lightspeed.app/quick-start/authentication/authorization-overview
- https://developers.flipdish.com/docs/api-overview

## 9. 국내 제품 상세

### 토스플레이스

국내 제품 중 유일하게 공식 도움말과 개발자 문서를 모두 확인할 수 있었다.

본사, 매장, 대리점 3계층으로 대시보드를 나눈다. 본사 상품 개념이 있고 기존 매장에서 불러오거나 엑셀로 등록한다. 등록 후 적용 대상 매장을 골라 적용하며 즉시 반영된다.

매장별 가격과 노출을 설정할 수 있다. 국내 제품 중 매장별 가격 재정의가 도움말 수준에서 확인된 유일한 사례다.

편집권은 매장 단위 토글로 조절한다. 본사만 수정 가능으로 설정하면 그 매장은 포스에서 개별 수정을 할 수 없다. 상품 단위가 아니라 매장 단위다.

매장 개설 권한이 본사가 아니라 대리점에 있다. 점주 동의가 전제다. 동의를 받지 않으면 매출을 볼 수 없지만 상품은 미리 등록할 수 있다.

매장 그룹 기능이 있다. 지역별, 직영과 가맹으로 묶어 매출을 합산하고 비교한다.

- https://tossplace.gitbook.io/guide
- https://toss.oopy.io/1d9714bb-fde7-805d-a72e-cd14c8e20b2c

외부 연동 API를 제공한다. 인증은 접근 키와 비밀 키를 헤더에 넣는 방식이며 OAuth가 아니다. 경로가 매장 단위다. 카탈로그는 조회 전용이고 생성과 수정 API가 없다. 대신 항목 생성, 수정, 삭제 웹훅을 제공한다.

품절은 판매중과 품절 상태값으로 조회된다. 문서는 품절 상태가 표기용 정보이며 주문 불가를 뜻하지 않는다고 밝힌다. 가격은 고정, 변동, 단위 유형으로 나뉘고 매장 식사와 포장별로 다르게 둘 수 있다. 호출 제한은 매장별 초당 10회, 최대 100회다.

- https://docs.tossplace.com/reference/open-api/intro.html
- https://docs.tossplace.com/reference/open-api/catalog.html

### 페이히어

본사 통합 관리 제품이 있다. 본사에서 한 번 수정하면 전 지점에 즉시 반영된다고 안내한다. 다만 매장별 가격 재정의, 품절 주체, 권한 등급은 공개 문서에 없다.

수발주 관리, 기기 원격 관리, 점검 자동화를 별도 기능으로 제공한다.

팝업과 행사 대상 단기 임대 서비스가 있었으나 현재 중단 상태다. 장비 임대이지 매장 관리 기능이 아니다.

- https://payhere.in/blog/franchise-store-management-guide-sales-fees-2026/

### 티오더

프랜차이즈 본사용 가맹점 관리 페이지를 운영한다. 메뉴 일괄 관리와 매장별 적용을 언급하나 가격 재정의인지 노출 제어인지 구분되지 않는다. 마케팅 문구 수준이다.

### 미조사

오케이포스, 포스뱅크, KT 유어오더, LG U+ 하이오더, 오더퀸, 배달의민족 사장님 도구, 먼슬리키친은 확인하지 못했다. 대부분 화면을 스크립트로 그리는 구조여서 본문을 읽을 수 없었다. 기능이 없다는 뜻이 아니라 확인하지 못했다는 뜻이다.

## 10. Toast와 Square 상세

### 매장 편집 권한

Toast는 매장이 바꿀 수 있는 항목을 권한으로 정확히 넷으로 제한한다.

1. 메뉴 그룹에 항목 추가와 제거
2. 옵션 그룹에 옵션 추가와 제거
3. 그룹 안의 순서 변경
4. 메뉴 항목의 매장별 가격 지정

항목명, 사이즈, 기본가는 본사 통제로 남는다. 권한이 없으면 가격 설정이 화면에서 비활성으로 표시된다.

- https://doc.toasttab.com/doc/platformguide/adminUnderstandingMenuEditingPermissionsForEnterprises.html

Square 프랜차이즈는 본사가 일곱 개 항목을 토글로 허용하거나 막는다.

항목명과 설명 수정, 가격 수정, 연결 수정, 재고코드 수정, 이미지 수정, 판매 불가 항목 제거, 중앙 메뉴 사본에 항목 추가다.

- https://squareup.com/help/us/en/article/8198-manage-menus-across-franchises-with-the-menu-settings-page

Toast는 매장 접근 권한과 웹 조회 권한을 별도 축으로 둔다. 매장 단말에 로그인하지 않으면서 그룹 리포팅 권한만 줄 수 있다.

- https://doc.toasttab.com/doc/platformguide/adminAssigningRestaurantGroupLevelPermissions.html

### 로컬 수정의 분리

Square에는 설계상 중요한 규칙이 있다. 가맹점이 항목명, 가격, 재고코드, 이미지를 로컬에서 수정하면 그 필드는 중앙 배포를 더 이상 받지 않는다.

- https://squareup.com/help/us/en/article/8512-troubleshoot-item-issues-with-square-for-franchises

이 규칙을 모르면 본사가 배포했는데 일부 매장만 반영되지 않는 현상을 설명할 수 없다.

### 품절 처리

Toast는 품절에 발행이 필요 없다. 즉시 적용된다. 다만 전 매장 일괄 품절 기능은 문서에 없다. 한 번에 한 매장씩이다.

기본 자동 복구가 없고, 옵션 기능으로 복구 스케줄을 둔다. 충돌하는 스케줄을 막지 않으며 우선순위를 보장하지 않는다고 명시한다.

- https://doc.toasttab.com/doc/platformguide/adminSettingInventoryStatusForMenuItems.html
- https://doc.toasttab.com/doc/platformguide/plartformAutomaticallyRefreshingInventory.html

복제로 만든 같은 이름 항목은 한쪽을 품절해도 다른 쪽이 풀려 있다. 복제 기반 배포는 품절 전파를 깨고 버전 기반 배포는 유지한다.

- https://support.toasttab.com/article/When-I-86-an-item-why-doesn-t-it-86-itself-in-another-menu

Square는 영업일 종료 시 품절이 기본으로 해제된다. 별도로 복구 시각과 주기를 지정할 수 있다.

- https://squareup.com/help/us/en/article/8495-beta-item-availability

Toast는 오프라인 중 메뉴 편집이 비활성화되어 품절 처리가 불가능하다.

- https://support.toasttab.com/en/article/Using-Toast-in-Offline-Mode

### 단말 반영 시간

Square는 항목 수정이 모든 단말에 반영되기까지 최대 10분이 걸린다고 명시한다. 반영되지 않으면 새 주문을 시작하거나 앱을 재시작하라고 안내한다. 단말이 로컬 사본을 쓴다는 뜻이다.

키오스크 메뉴는 100개 항목 이하를 권고한다. 초과하면 동기화가 지연된다.

- https://squareup.com/help/us/en/article/8380-troubleshoot-the-square-kiosk-app

### 채널별 가격

두 제품 모두 채널별 가격을 1급 기능으로 제공하지 않는다. 배달앱 인상률로만 우회한다.

Toast는 매장별 가격이 자사 온라인 주문과 테이크아웃 앱에서 동작하지 않는다. 시간대별 가격은 전 채널에서 동작한다. 이 비대칭을 문서가 명시한다.

- https://doc.toasttab.com/doc/platformguide/adminToastProductChannelSupportForAdvancedPricingFeatures.html

### 외부 연동 인증

Toast 인증은 OAuth2가 아니다. 접근 키와 비밀 키를 본문에 담아 로그인하고 토큰을 받는 자체 방식이다. Square는 OAuth2 승인 코드 방식이다.

- https://doc.toasttab.com/doc/devguide/authentication.html

앞서 정리한 "사실상 표준은 OAuth2 client credentials"는 정정한다. Toast는 자체 방식, Square는 승인 코드, Flipdish는 client credentials, Lightspeed는 승인 코드, 토스플레이스는 키 쌍 방식이다. 통일된 표준이 없다.

Toast 메뉴 API는 읽기 전용이며 발행된 데이터만 반환한다. 메뉴 JSON은 발행 시점에만 다시 만들어진다. 웹훅으로 발행을 알리고 조회로 가져가는 구조다. 웹훅을 쓰지 않으면 1~5분 주기, 쓰면 30분 백업 주기를 권고한다.

- https://doc.toasttab.com/doc/devguide/apiMenusWebhook.html

### 매장 그룹 정리

앞의 정리를 보완한다.

Toast는 매장 그룹을 만들 수 있고 중첩할 수 있으며 한 매장이 여러 그룹에 속할 수 있다. 다만 리포트에서 확인된 것은 필터 사용이며, 그룹을 집계 행으로 놓고 그룹 대 그룹을 비교하는 화면은 확인되지 않았다.

Square는 프랜차이즈 제품에만 매장 그룹이 있다. 기본 계정에는 없다. 그룹 리포팅을 조회할 수 있다고 적혀 있으나 구체 화면은 확인되지 않았다.

두 제품 모두 그룹에 기간 속성이 없다.

## 11. 국내 제품 종합

제품 9종을 확인한 결과다. 확인 수준을 먼저 밝힌다.

| 구분 | 제품 |
| --- | --- |
| 공식 매뉴얼 확보 | 토스플레이스, 오케이포스, 배달의민족 |
| 매뉴얼 일부와 마케팅 | 페이히어, 티오더 |
| 마케팅만 | 하이오더 |
| 접근 실패 | 오더퀸, 먼슬리키친, 포스뱅크, 배민오더, 배민상회 |

전제 두 가지를 정정한다. KT의 테이블오더 제품은 하이오더이며 유어오더는 어느 공식 채널에서도 확인되지 않는다. 하이오더는 LG유플러스가 아니라 KT 제품이다.

### 본사 셀프서비스는 드물다

본사가 직접 조작하는 콘솔을 갖춘 제품은 토스플레이스뿐이다.

배달의민족, 티오더, 하이오더는 공급사 접수 채널을 거친다. 본사가 메일이나 배너로 접수하면 운영팀이 작업한다. 배달의민족은 신규 메뉴에 최소 10영업일이 걸린다고 안내한다.

오케이포스는 본사 등록을 대리점이 신청하고 공급사가 처리한다. 매장 등록도 대리점 화면에서 한다.

본사 셀프서비스를 당연한 전제로 두면 근거 없는 가정이 된다.

### 배포는 내려받기가 지배적이다

오케이포스는 POS가 재부팅 시점이나 개점 시점에 저장한다. 키오스크는 주문 대기 10분 무조작 또는 결제 시점에 약 2초간 반영한다. 반영 항목은 상품명, 가격, 이미지, 바코드, 세트, 사이드, 품절, 포장할인이다.

즉시 반영을 명시한 것은 토스플레이스뿐이다.

오프라인 대응은 국내 9개 제품 전부에서 확인되지 않았다.

### 품절은 예외 없이 매장 주체다

국내 9개 제품 어디에서도 본사의 일괄 품절 제어 근거가 없다.

배달의민족은 본사메뉴판을 쓰는 가게도 품절과 숨김을 매장이 직접 한다. 본사 일괄 숨김은 신규 메뉴 등록 시에만 가능하고 기존 메뉴는 삭제 후 재등록해야 한다.

오케이포스는 관리 화면, POS, 키오스크 모든 기기에서 품절 처리와 해제가 가능하다고 적는다.

본사 통제형 품절이 필요하면 신규 요구사항으로 정의해야 한다.

### 권한은 매장 단위 잠금이다

국내 관행은 항목 단위 권한이 아니라 매장 편집권 켜기와 끄기다.

토스플레이스는 본사만 수정 가능 토글, 배달의민족은 본사메뉴판과 가게메뉴판 타입, 티오더는 본사 정책에 따른 점주 앱 차단으로 각각 구현한다.

예외는 오케이포스다. 그룹관리자를 두고 사원별 메뉴 권한을 개별 지정한다.

### 가격은 매장에, 구성은 본사에

매장별 가격 재정의가 확인된 국내 제품은 토스플레이스와 배달의민족이다.

배달의민족은 본사메뉴판을 쓰더라도 가격만은 매장이 바꿀 수 있게 열어 둔다. 매장이 바꿀 수 없는 것은 메뉴 추가, 메뉴명, 순서, 설명, 옵션, 대표메뉴다.

오케이포스는 판매가가 매장 속성이라 구조가 다르다. 티오더는 가격이 POS에 귀속되어 있어 성립하기 어렵다.

가격은 매장에 두고 메뉴 구성은 본사가 통제하는 경계선이 국내 관행에 가깝다.

### 한시 매장은 전부 부재하며 구조적으로 어렵다

배달의민족의 광고 캠페인은 캠페인 단위 메뉴 수정이 불가하다. 주소별로 메뉴나 운영시간을 달리하려면 가게를 새로 추가해야 하고, 가게 추가는 서류 접수 절차다. 단기 운영에 맞지 않는다.

오케이포스는 개설과 폐점이 대리점을 거쳐야 한다.

대안은 범용 매장 그룹 기능뿐이다. 토스플레이스와 오케이포스가 제공한다.

### 공개 API는 하나뿐이다

국내에서 공개 API 규격을 확인한 것은 토스플레이스뿐이다.

오케이포스는 표준 API 제공이라는 목차 항목이 있으나 본문이 비어 있다.

배달의민족은 Windows 라이브러리 기반이며 인증이 자체 개발, 진단 통과, 최종 연동 테스트의 3단계다. 서버 대 서버 연동을 전제한 설계가 성립하지 않는다.

## 7. 추가 확인 필요

- 오케이포스, 유어오더, 먼슬리키친의 본사 관리 기능
- 국내 POS의 외부 연동 API 제공 여부와 인증 방식
- Olo의 본사 메뉴와 매장 메뉴 권한 경계
- 배달의민족 본사메뉴판에서 가맹점이 수정 가능한 항목의 정확한 목록
- Toast 다매장에서 품절 상태가 매장 간 공유되는지 여부
