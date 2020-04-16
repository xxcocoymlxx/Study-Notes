Hello there <?= $_REQUEST["name"] ?>

<xmp>
<?php $banner=system("/usr/bin/printerbanner -w 40 \"$_REQUEST[name]\""); ?>
<?= $banner ?>
</xmp>
