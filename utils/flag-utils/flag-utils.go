package flagutils

import "flag"

func CheckForArgsCount(count int) bool {
	if len(flag.Args()) >= count {
		return true
	} else {
		return false
	}
}
