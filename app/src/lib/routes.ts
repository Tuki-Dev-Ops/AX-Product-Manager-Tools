/** 화면 주소. 새로 고치거나 주소를 나눠도 같은 자리가 열린다. */
export const routes = {
  home: '/',
  changes: '/changes',
  doc: (no: number | string = ':no', sec?: number | string, flow?: string) =>
    ['/doc', no, sec, flow].filter((v) => v !== undefined && v !== '').join('/'),
  wireframe: (id = ':id') => `/wireframe/${id}`,
} as const
