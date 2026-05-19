import time
import numpy as np

class BanCo:
    def __init__(self, kich_thuoc=9):
        self.kich_thuoc = kich_thuoc
        self.ma_tran = np.full((kich_thuoc, kich_thuoc), '.')
        self.so_nuoc_di = 0

    def in_ban_co(self):
        print("\n   " + " ".join([str(i) for i in range(self.kich_thuoc)]))
        for r in range(self.kich_thuoc):
            print(f"{r}  " + " ".join(self.ma_tran[r]) + f"  {r}")
        print("   " + " ".join([str(i) for i in range(self.kich_thuoc)]) + "\n")

    def danh_co(self, dong, cot, nguoi_choi):
        if 0 <= dong < self.kich_thuoc and 0 <= cot < self.kich_thuoc and self.ma_tran[dong][cot] == '.':
            self.ma_tran[dong][cot] = nguoi_choi
            self.so_nuoc_di += 1
            return True
        return False

    def huy_nuoc_di(self, dong, cot):
        if 0 <= dong < self.kich_thuoc and 0 <= cot < self.kich_thuoc and self.ma_tran[dong][cot] != '.':
            self.ma_tran[dong][cot] = '.'
            self.so_nuoc_di -= 1

    def kiem_tra_day(self):
        return self.so_nuoc_di == self.kich_thuoc * self.kich_thuoc

    def kiem_tra_thang(self, nguoi_choi):
        cac_huong = [(0, 1), (1, 0), (1, 1), (1, -1)]
        for r in range(self.kich_thuoc):
            for c in range(self.kich_thuoc):
                if self.ma_tran[r][c] == nguoi_choi:
                    for dr, dc in cac_huong:
                        dem = 1
                        for i in range(1, 4):
                            nr, nc = r + dr * i, c + dc * i
                            if 0 <= nr < self.kich_thuoc and 0 <= nc < self.kich_thuoc and self.ma_tran[nr][nc] == nguoi_choi:
                                dem += 1
                            else:
                                break
                        if dem == 4:
                            return True
        return False

    def sinh_nuoc_di_hop_le(self):
        if self.so_nuoc_di == 0:
            return [(self.kich_thuoc // 2, self.kich_thuoc // 2)]
        danh_sach_nuoc_di = set()
        for r in range(self.kich_thuoc):
            for c in range(self.kich_thuoc):
                if self.ma_tran[r][c] != '.':
                    for dr in range(-2, 3):
                        for dc in range(-2, 3):
                            nr, nc = r + dr, c + dc
                            if 0 <= nr < self.kich_thuoc and 0 <= nc < self.kich_thuoc and self.ma_tran[nr][nc] == '.':
                                danh_sach_nuoc_di.add((nr, nc))
        return list(danh_sach_nuoc_di)

class AI_Caro:
    def __init__(self, quan_may='O', quan_nguoi='X', do_sau_toi_da=3):
        self.quan_may = quan_may
        self.quan_nguoi = quan_nguoi
        self.do_sau_toi_da = do_sau_toi_da
        self.so_trang_thai_da_xet = 0

    def cham_diem_chuoi(self, chuoi):
        diem = 0
        dem_may = chuoi.count(self.quan_may)
        dem_nguoi = chuoi.count(self.quan_nguoi)
        dem_trong = chuoi.count('.')

        if dem_may == 4:
            diem += 100000
        elif dem_nguoi == 4:
            diem -= 100000
        elif dem_may == 3 and dem_trong == 1:
            diem += 1000
        elif dem_nguoi == 3 and dem_trong == 1:
            diem -= 5000
        elif dem_may == 2 and dem_trong == 2:
            diem += 10
        elif dem_nguoi == 2 and dem_trong == 2:
            diem -= 50

        return diem

    def cham_diem_ban_co(self, ban_co):
        if ban_co.kiem_tra_thang(self.quan_may): return 1000000
        if ban_co.kiem_tra_thang(self.quan_nguoi): return -1000000
        if ban_co.kiem_tra_day(): return 0

        tong_diem = 0
        kt = ban_co.kich_thuoc
        
        for r in range(kt):
            for c in range(kt - 3):
                tong_diem += self.cham_diem_chuoi([ban_co.ma_tran[r][c+i] for i in range(4)])
        for r in range(kt - 3):
            for c in range(kt):
                tong_diem += self.cham_diem_chuoi([ban_co.ma_tran[r+i][c] for i in range(4)])
        for r in range(kt - 3):
            for c in range(kt - 3):
                tong_diem += self.cham_diem_chuoi([ban_co.ma_tran[r+i][c+i] for i in range(4)])
        for r in range(3, kt):
            for c in range(kt - 3):
                tong_diem += self.cham_diem_chuoi([ban_co.ma_tran[r-i][c+i] for i in range(4)])
                
        return tong_diem

    def minimax(self, ban_co, do_sau, luot_may):
        self.so_trang_thai_da_xet += 1
        if do_sau == 0 or ban_co.kiem_tra_thang(self.quan_may) or ban_co.kiem_tra_thang(self.quan_nguoi) or ban_co.kiem_tra_day():
            return self.cham_diem_ban_co(ban_co), None

        cac_nuoc_di = ban_co.sinh_nuoc_di_hop_le()
        nuoc_di_tot_nhat = None

        if luot_may:
            diem_max = -float('inf')
            for nuoc_di in cac_nuoc_di:
                ban_co.danh_co(nuoc_di[0], nuoc_di[1], self.quan_may)
                diem_danh_gia, _ = self.minimax(ban_co, do_sau - 1, False)
                ban_co.huy_nuoc_di(nuoc_di[0], nuoc_di[1])
                if diem_danh_gia > diem_max:
                    diem_max, nuoc_di_tot_nhat = diem_danh_gia, nuoc_di
            return diem_max, nuoc_di_tot_nhat
        else:
            diem_min = float('inf')
            for nuoc_di in cac_nuoc_di:
                ban_co.danh_co(nuoc_di[0], nuoc_di[1], self.quan_nguoi)
                diem_danh_gia, _ = self.minimax(ban_co, do_sau - 1, True)
                ban_co.huy_nuoc_di(nuoc_di[0], nuoc_di[1])
                if diem_danh_gia < diem_min:
                    diem_min, nuoc_di_tot_nhat = diem_danh_gia, nuoc_di
            return diem_min, nuoc_di_tot_nhat

    def alpha_beta(self, ban_co, do_sau, alpha, beta, luot_may):
        self.so_trang_thai_da_xet += 1
        if do_sau == 0 or ban_co.kiem_tra_thang(self.quan_may) or ban_co.kiem_tra_thang(self.quan_nguoi) or ban_co.kiem_tra_day():
            return self.cham_diem_ban_co(ban_co), None

        cac_nuoc_di = ban_co.sinh_nuoc_di_hop_le()
        nuoc_di_tot_nhat = None

        if luot_may:
            diem_max = -float('inf')
            for nuoc_di in cac_nuoc_di:
                ban_co.danh_co(nuoc_di[0], nuoc_di[1], self.quan_may)
                diem_danh_gia, _ = self.alpha_beta(ban_co, do_sau - 1, alpha, beta, False)
                ban_co.huy_nuoc_di(nuoc_di[0], nuoc_di[1])
                if diem_danh_gia > diem_max:
                    diem_max, nuoc_di_tot_nhat = diem_danh_gia, nuoc_di
                alpha = max(alpha, diem_danh_gia)
                if beta <= alpha: break
            return diem_max, nuoc_di_tot_nhat
        else:
            diem_min = float('inf')
            for nuoc_di in cac_nuoc_di:
                ban_co.danh_co(nuoc_di[0], nuoc_di[1], self.quan_nguoi)
                diem_danh_gia, _ = self.alpha_beta(ban_co, do_sau - 1, alpha, beta, True)
                ban_co.huy_nuoc_di(nuoc_di[0], nuoc_di[1])
                if diem_danh_gia < diem_min:
                    diem_min, nuoc_di_tot_nhat = diem_danh_gia, nuoc_di
                beta = min(beta, diem_danh_gia)
                if beta <= alpha: break
            return diem_min, nuoc_di_tot_nhat


def bat_dau_choi():
    print(" CHƯƠNG TRÌNH CARO AI ")
    
    print("Chọn thuật toán:")
    print("1. Thuật toán Minimax (Level 1)")
    print("2. Thuật toán Alpha-Beta (Level 2)")
    
    while True:
        lua_chon_thuat_toan = input("Lựa chọn (1 hoặc 2): ").strip()
        if lua_chon_thuat_toan in ['1', '2']:
            break
        print("Lỗi: Vui lòng nhập 1 hoặc 2.")
    
    while True:
        try:
            do_sau_nhap_vao = int(input("Nhập độ sâu tìm kiếm (VD: 2 hoặc 3): ").strip())
            if do_sau_nhap_vao >= 1:
                break
            print("Độ sâu phải >= 1.")
        except ValueError:
            print("Lỗi: Vui lòng nhập số nguyên.")

    ban_co = BanCo(kich_thuoc=9)
    may_tinh = AI_Caro(do_sau_toi_da=do_sau_nhap_vao)
    ban_co.in_ban_co()

    while True:
        while True:
            try:
                nuoc_di = input("Lượt của bạn (X) - Nhập 'dòng cột' (vd: 4 4): ")
                dong, cot = map(int, nuoc_di.split())
                if ban_co.danh_co(dong, cot, 'X'): break
                else: print("Nước đi không hợp lệ!")
            except: print("Vui lòng nhập 2 số nguyên.")
            
        ban_co.in_ban_co()
        if ban_co.kiem_tra_thang('X'):
            print("Người chơi thắng!"); break
        if ban_co.kiem_tra_day():
            print("Hòa!"); break

        print(f"\nMáy đang tính toán (Độ sâu: {do_sau_nhap_vao})...")
        nuoc_di_tot_nhat = None
        
        may_tinh.so_trang_thai_da_xet = 0
        thoi_gian_bat_dau = time.perf_counter()
        
        if lua_chon_thuat_toan == '1':
            diem, nuoc_di_tot_nhat = may_tinh.minimax(ban_co, do_sau_nhap_vao, True)
            thoi_gian_chay = time.perf_counter() - thoi_gian_bat_dau
            print(f"[MINIMAX] Nước đi: {nuoc_di_tot_nhat} | Điểm: {diem} | Trạng thái xét: {may_tinh.so_trang_thai_da_xet} | Thời gian: {thoi_gian_chay:.4f}s")
            
        elif lua_chon_thuat_toan == '2':
            diem, nuoc_di_tot_nhat = may_tinh.alpha_beta(ban_co, do_sau_nhap_vao, -float('inf'), float('inf'), True)
            thoi_gian_chay = time.perf_counter() - thoi_gian_bat_dau
            print(f"[ALPHA-BETA] Nước đi: {nuoc_di_tot_nhat} | Điểm: {diem} | Trạng thái xét: {may_tinh.so_trang_thai_da_xet} | Thời gian: {thoi_gian_chay:.4f}s")

        if nuoc_di_tot_nhat:
            ban_co.danh_co(nuoc_di_tot_nhat[0], nuoc_di_tot_nhat[1], 'O')
        else:
            print("Máy không tìm được nước đi.")
            break
            
        ban_co.in_ban_co()
        if ban_co.kiem_tra_thang('O'):
            print("Máy thắng!"); break
        if ban_co.kiem_tra_day():
            print("Hòa!"); break

if __name__ == "__main__":
    bat_dau_choi()
