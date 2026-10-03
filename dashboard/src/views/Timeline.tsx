import type { Dataset } from '../data/types';
export function Timeline({ data }: { data: Dataset; params?: URLSearchParams }) {
  void data;
  return <div className="wrap page-head"><p className="eyebrow"><span className="tick" />In progress</p><h1 className="display">This view is being built.</h1></div>;
}
