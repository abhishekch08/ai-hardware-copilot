#define GPIO_REG_EN 17
#define REG_CTRL_SLEEP 0x02

void enable_regulator(void) {
    (void)GPIO_REG_EN;
}

void enter_low_power(void) {
    (void)REG_CTRL_SLEEP;
}
