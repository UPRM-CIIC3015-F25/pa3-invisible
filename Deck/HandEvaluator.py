from Cards.Card import Card, Rank

# TODO (TASK 3): Implement a function that evaluates a player's poker hand.
#   Loop through all cards in the given 'hand' list and collect their ranks and suits.
#   Use a dictionary to count how many times each rank appears to detect pairs, three of a kind, or four of a kind.
#   Sort these counts from largest to smallest. Use another dictionary to count how many times each suit appears to check
#   for a flush (5 or more cards of the same suit). Remove duplicate ranks and sort them to detect a
#   straight (5 cards in a row). Remember that the Ace (rank 14) can also count as 1 when checking for a straight.
#   If both a straight and a flush occur in the same suit, return "Straight Flush". Otherwise, use the rank counts
#   and flags to determine if the hand is: "Four of a Kind", "Full House", "Flush", "Straight", "Three of a Kind",
#   "Two Pair", "One Pair", or "High Card". Return a string with the correct hand type at the end.
def evaluate_hand(hand: list[Card]):
    if not hand:
        return "High Card"

    rk_lst = []
    st_lst = []
    for c in hand:
        rk_lst.append(c.rank.value)
        st_lst.append(c.suit)

    rk_cnt = {}
    for rv in rk_lst:
        if rv in rk_cnt:
            rk_cnt[rv] += 1
        else:
            rk_cnt[rv] = 1

    st_cnt = {}
    for s in st_lst:
        if s in st_cnt:
            st_cnt[s] += 1
        else:
            st_cnt[s] = 1

    cnt_vals = []
    for v in rk_cnt.values():
        cnt_vals.append(v)
    cnt_vals.sort(reverse=True)

    flg_flush = False
    fl_suit = None
    for s, ct in st_cnt.items():
        if ct >= 5:
            flg_flush = True
            fl_suit = s
            break

    def has_stra(vs):
        if not vs:
            return False
        uni = list(set(vs))
        uni.sort()
        if 14 in uni:
            # ace low
            uni2 = list(uni)
            uni2.append(1)
            uni2 = list(set(uni2))
            uni2.sort()
        else:
            uni2 = uni

        mx = 1
        cur = 1
        i2 = 1
        while i2 < len(uni2):
            if uni2[i2] == uni2[i2 - 1] + 1:
                cur += 1
                if cur > mx:
                    mx = cur
            elif uni2[i2] != uni2[i2 - 1]:
                cur = 1
            i2 += 1
        return mx >= 5

    flg_stra = has_stra(rk_lst)

    flg_strafl = False
    if flg_flush and fl_suit is not None:
        rk_sf = []
        for c in hand:
            if c.suit == fl_suit:
                rk_sf.append(c.rank.value)
        if has_stra(rk_sf):
            flg_strafl = True

    if flg_strafl:
        return "Straight Flush"
    if cnt_vals and cnt_vals[0] == 4:
        return "Four of a Kind"
    if cnt_vals and cnt_vals[0] == 3:
        has_pair = False
        for v in cnt_vals[1:]:
            if v >= 2:
                has_pair = True
                break
        if has_pair:
            return "Full House"
        return "Three of a Kind"
    if flg_flush:
        return "Flush"
    if flg_stra:
        return "Straight"
    if cnt_vals and cnt_vals[0] == 2:
        pair_ct = 0
        for v in cnt_vals:
            if v == 2:
                pair_ct += 1
        if pair_ct >= 2:
            return "Two Pair"
        return "One Pair"
    return "High Card"
