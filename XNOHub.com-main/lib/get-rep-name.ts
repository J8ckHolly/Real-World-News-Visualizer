import { RepsData } from '@/data/defualtMergedRepsData';

export const getRepName = (account: string) => {
  const rep = RepsData.find((rep) => rep.account === account);
  return rep ? rep.account_formatted : null;
};
